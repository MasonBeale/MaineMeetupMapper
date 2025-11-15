import requests
from bs4 import BeautifulSoup
import json
import lxml
import asyncio
from playwright.async_api import async_playwright

async def scrape_event(page, url):
    await page.goto(url)
    try:
        await page.wait_for_selector('.contentRender_12', timeout=10000)
    except:
        print(f"Warning: .contentRender_12 not found on {url}")

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # Title Extraction
    content_div = soup.find(class_='contentRender_12')
    title = ''
    if content_div:
        h1 = content_div.find('h1')
        title = h1.get_text(strip=True) if h1 else ''
    else:
        h1 = soup.find('h1')
        title = h1.get_text(strip=True) if h1 else ''

    # -------- Extract detail-info-bar and Email href --------
    detail_info_bar = soup.find(class_='detail-info-bar')
    detail_info_data = {}
    email_href = ""
    if detail_info_bar:
        for child in detail_info_bar.find_all('div', recursive=False):
            label = child.find('span', class_='label')
            value = child.find('span', class_='value')
            if label and value:
                key = label.get_text(strip=True)
                val = value.get_text(strip=True)
                detail_info_data[key] = val
            else:
                # Look for anchor tags labeled "Email"
                for a in child.find_all('a', href=True):
                    if "Email" in a.get_text(strip=True):
                        email_href = a['href']
                        break
                fallback_text = child.get_text(separator='\n', strip=True)
                if fallback_text:
                    detail_info_data[f"info_{len(detail_info_data)+1}"] = fallback_text
    else:
        print(f"Warning: .detail-info-bar not found on {url}")
    # --------------------------------------------------------

    # -------- Extract #descriptionTab contents --------
    description_tab_data = ''
    description_tab = soup.find(id='descriptionTab')
    if description_tab:
        description_tab_data = description_tab.get_text(separator='\n', strip=True)
    else:
        print(f"Warning: #descriptionTab not found on {url}")
    # --------------------------------------------------

    return {
        'url': url,
        'title': title,
        'detail_info_bar': detail_info_data,
        'descriptionTab': description_tab_data,
        'email_href': email_href
    }

async def main():
    sitemap_url = "https://www.mainetourism.com/sitemap.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; ScraperBot/1.0)'
    }

    response = requests.get(sitemap_url, headers=headers)
    response.raise_for_status()
    sitemap_soup = BeautifulSoup(response.content, 'lxml-xml')
    urls = [loc.get_text() for loc in sitemap_soup.find_all('loc') if '/event/' in loc.get_text()]

    print(f"Found {len(urls)} event URLs in sitemap.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        events_data = []
        for idx, url in enumerate(urls, 1):
            print(f"Scraping {idx}/{len(urls)}: {url}")
            data = await scrape_event(page, url)
            events_data.append(data)

        await browser.close()

    with open('mainetourism_events_full.json', 'w', encoding='utf-8') as f:
        json.dump(events_data, f, indent=4, ensure_ascii=False)

    print(f"Scraping complete! Data saved to 'mainetourism_events_full.json'.")

if __name__ == "__main__":
    asyncio.run(main())
