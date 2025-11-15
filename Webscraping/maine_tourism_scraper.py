"""
maine_tourism_scraper.py
---

Python script to scrape event data from the Maine Tourism website.
Utilizes Playwright for dynamic content rendering and BeautifulSoup for HTML parsing.
Returns JSON file with comprehensive event details including title,
description, contact info, location, and event time.

Author: Kristina Zbinden using Perplexity AI
Date: 11/13/2025
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import asyncio
from playwright.async_api import async_playwright

async def scrape_event(page, url):
    await page.goto(url)
    try:
        await page.wait_for_selector('.contentRender_12', timeout=10000)
    except:
        print(f"Warning: .contentRender_12 not found on {url}")

    # Initialize variables
    description_tab_data = ""
    title = ''
    detail_info_data = {}
    email_address = ""
    location = ""
    start_time = ""
    end_time = ""
    event_date = ""

    # Date pattern to match various date formats found in the text
    date_pattern = re.compile(
        r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|'
        r'January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s\d{1,2}'
        r'(?:,\s?\d{4})?)\b',
        re.IGNORECASE
    )

    # Extacting page content
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # Title Extraction
    content_div = soup.find(class_='contentRender_12')
    if content_div:
        h1 = soup.find('h1')
        title = h1.get_text(strip=True) if h1 else ''

    # Date Extraction - Try extracting event_date from #priority-info > dd first
    priority_info = soup.find(class_='priority-info')
    if priority_info:
        dd_tags = priority_info.find_all('dd')
        for dd in dd_tags:
            dd_text = dd.get_text(strip=True)
            # Find all matching dates in this dd text
            date_matches = date_pattern.findall(dd_text)
            if date_matches:
                event_date = date_matches[0]
                break  # Stop after first found date


    # Extact .detail-info-bar contents
    detail_info_bar = soup.find(class_='detail-info-bar')

    if detail_info_bar:
        children = detail_info_bar.find_all('div', recursive=False)
        # Loop through each child div in .detail-info-bar
        for idx, child in enumerate(children):
            label = child.find('span', class_='label')
            value = child.find('span', class_='value')
            if label and value:
                key = label.get_text(strip=True)
                val = value.get_text(strip=True)
                detail_info_data[key] = val
            else:
                # Find anchor tags labeled "Email" for email extraction
                for a in child.find_all('a', href=True):
                    if "Email" in a.get_text(strip=True):
                        email_address = a['href']
                        break
                if email_address.startswith("mailto:"):
                    email_address = email_address[len("mailto:"):]  # Removes 'mailto:'
                fallback_text = child.get_text(separator='\n', strip=True)
                if fallback_text:
                    detail_info_data[f"info_{len(detail_info_data)+1}"] = fallback_text

            # Assign by position: 0-based index
            if idx == 0: 
                location = child.get_text(separator='\n', strip=True)

            # Check for start/end time in idx 1 or within existing loop:
            if idx in (1, 2):
                text = child.get_text(separator='\n', strip=True)
                
                # Extract event times from substring after "Time:" if present
                time_pos = text.find("Time:")
                if time_pos != -1:
                    time_line = text[time_pos + len("Time:"):].strip()
                    time_line = time_line.splitlines()[0].strip()
                    if ' to ' in time_line:
                        start_time, end_time = [t.strip() for t in time_line.split(' to ', 1)]
                    else:
                        start_time = time_line.strip()

                # Extract dates from the entire text block
                if not event_date:  # Only update if not set above
                    date_matches = date_pattern.findall(text)
                    if date_matches:
                        event_date = date_matches[0]

    else:
        print(f"Warning: Data not found on {url}")

    # Extract #descriptionTab content for event description
    description_tab_data = ''
    description_tab = soup.find(id='descriptionTab')
    if description_tab:
        description_tab_data = description_tab.get_text(separator='\n', strip=True)
    else:
        description_tab_data = ''

    # Return compiled data
    return {
        'url': url,
        'title': title,
        'descriptionTab': description_tab_data,
        'email_address': email_address, 
        'location' : location,
        'start_time' : start_time,
        'end_time' : end_time,
        'date' : event_date
    }

async def main():
    # Fetch sitemap from site to be scraped
    sitemap_url = "https://www.mainetourism.com/sitemap.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; ScraperBot/1.0)'
    }

    response = requests.get(sitemap_url, headers=headers)
    response.raise_for_status()
    sitemap_soup = BeautifulSoup(response.content, 'lxml-xml')
    # Extract event URLs from sitemap
    urls = [loc.get_text() for loc in sitemap_soup.find_all('loc') if '/event/' in loc.get_text()]

    print(f"Found {len(urls)} event URLs in sitemap.")

    # Scrape each event URL using Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        events_data = []
        for idx, url in enumerate(urls, 1):
            print(f"Scraping {idx}/{len(urls)}: {url}")
            data = await scrape_event(page, url)
            events_data.append(data)

        await browser.close()

    # Save data to JSON file
    with open('mainetourism_events_data.json', 'w', encoding='utf-8') as f:
        json.dump(events_data, f, indent=4, ensure_ascii=False)

    print(f"Scraping complete! Data saved to 'mainetourism_events_data.json'.")

if __name__ == "__main__":
    asyncio.run(main())
