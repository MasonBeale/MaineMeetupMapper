"""
meetup_scraper.py
----------------------------------
A Python script that uses Selenium and BeautifulSoup
to scrape local in-person Meetup events in Portland, Maine,
within 18 miles from the Meetup.com website
and save them as structured JSON data.

Author: Mason Beale with help from GPT-5
Date: November 11, 2025
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import json

def scrape():
    url = "https://www.meetup.com/find/?source=EVENTS&eventType=inPerson&sortField=DATETIME&location=us--me--Portland"
    
    """
    Set up Selenium WebDriver with headless Chrome
    I got this directly from ChatGPT, i havent tried any other options so this may not be optimized
    """
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    driver = webdriver.Chrome(options=options)
    
    try:
        print("Loading page")
        driver.get(url)
        
        # checks that theres actually an event that loaded
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/events/']")))

        # activates a few scrolls until the whole page is loaded
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_round = 0
        while True:
            scroll_round += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                print(f"No more content after {scroll_round} scrolls.")
                break

            last_height = new_height


        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find our target elements
        event_links = soup.find_all('a', {
            'class': 'group inline size-full cursor-pointer hover:no-underline',
            'data-event-label': 'Event Card'
        })
        
        print(f"Found {len(event_links)} events")

        date_pattern = re.compile(r'([A-Za-z]{3}\s\d{1,2})')
        time_pattern = re.compile(r'(\d{1,2}:\d{2}\s[APM]{2})')
        attendees_pattern = re.compile(r'(\d+)')

        events_data = []
        
        for link in event_links:
  
            event_soup = BeautifulSoup(str(link), 'html.parser')
            
            event_data = {
                'title': event_soup.select_one('h3.ds2-m18').get_text(strip=True),
                'desc': event_soup.select_one('div.ds2-r14 > div.flex-shrink').get_text(strip=True) + " " + link["href"],
                'date': date_pattern.search(event_soup.select_one('time').get_text(strip=True)).group(1),
                'start_time': time_pattern.search(event_soup.select_one('time').get_text(strip=True)).group(1),
                'end_time': None,
                'max_capacity': None,
                'attendees': attendees_pattern.search(event_soup.select_one('span.ds2-m14').get_text(strip=True)).group(1)
            }
            events_data.append(event_data)
        
        with open("Webscraping/meetup_events.json", "w", encoding="utf-8") as f:
            json.dump(events_data, f, ensure_ascii=False, indent=4)
        
    finally:
        driver.quit()
scrape()