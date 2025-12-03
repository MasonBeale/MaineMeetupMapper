"""
eventbrite_scraper.py
----------------------------------
A Python script that uses Selenium to scrape venue/location data 
from Eventbrite events in Maine.
Author: Logan
Date: November 13, 2025
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import json
import re

def scrape_eventbrite_locations():
    """
    Scrape location/venue data from Eventbrite events in Maine
    """
    
    url = "https://www.eventbrite.com/d/me--maine/events/"
    
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    locations = []
    
    try:
        print("Loading Eventbrite page...")
        driver.get(url)
        
        print("Waiting for events to load...")
        time.sleep(5)
        
        # Scroll to load more events
        print("Scrolling to load events...")
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        print("Finding event elements...")
        # The <a> tag itself has the data-event-location attribute
        event_cards = driver.find_elements(By.CSS_SELECTOR, "a[data-event-location]")
        
        print(f"✓ Found {len(event_cards)} potential event elements\n")
        
        seen_venues = set()
        
        for card in event_cards:
            try:
                # Get venue/event name from aria-label on the <a> tag itself
                venue_name = "Unknown Venue"
                aria_label = card.get_attribute("aria-label")
                if aria_label and aria_label.startswith("View "):
                    venue_name = aria_label[5:].strip()  # Remove "View " prefix
                    # Truncate if too long
                    if len(venue_name) > 60:
                        venue_name = venue_name[:60]
                
                # Get location from data-event-location attribute
                location_text = card.get_attribute("data-event-location") or "Unknown"
                
                if not location_text or location_text == "Unknown":
                    continue
                
                # Parse location (format: "Portland, ME")
                city = location_text
                state = "ME"
                zip_code = "04101"
                
                if ',' in location_text:
                    parts = location_text.split(',')
                    city = parts[0].strip()
                    if len(parts) >= 2:
                        state = parts[1].strip()
                
                # Assign ZIP codes based on city
                zip_codes = {
                    'Portland': '04101',
                    'South Portland': '04106',
                    'Kennebunkport': '04046',
                    'Bangor': '04401',
                    'Augusta': '04330',
                    'Lewiston': '04240',
                    'Brunswick': '04011',
                    'Saco': '04072',
                    'Biddeford': '04005',
                    'Waterville': '04901',
                    'Gardiner': '04345',
                    'Millinocket': '04462',
                    'Carrabassett Valley': '04947',
                    'Bar Harbor': '04609',
                    'Ogunquit': '03907',
                    'Freeport': '04032',
                    'Camden': '04843',
                    'Rockland': '04841',
                    'Scarborough': '04074',
                    'Westbrook': '04092'
                }
                zip_code = zip_codes.get(city, '04101')
                
                venue_key = f"{venue_name}_{city}"
                
                if venue_key not in seen_venues and venue_name != "Unknown Venue":
                    seen_venues.add(venue_key)
                    
                    location = {
                        'venue_name': venue_name,
                        'address': city,  # Using city as address since street not available
                        'city': city,
                        'zip_code': zip_code
                    }
                    
                    locations.append(location)
                    print(f"{len(locations)}. {venue_name} - {city}, {zip_code}")
                    
                    if len(locations) >= 50:
                        break
                    
            except Exception as e:
                continue
        
        print(f"\n✓ Scraped {len(locations)} location entries")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()
    
    return locations


# Main execution
if __name__ == "__main__":
    print("="*60)
    print("Eventbrite Location Scraper - Maine")
    print("="*60 + "\n")
    
    locations = scrape_eventbrite_locations()
    
    if locations:
        # Save RAW scraped data
        df = pd.DataFrame(locations)
        df.to_csv('locations_raw.csv', index=False)
        print(f"\n✓ Saved {len(locations)} RAW locations to locations_raw.csv")
        
        # Also save as JSON
        with open('locations_raw.json', 'w', encoding='utf-8') as f:
            json.dump(locations, f, ensure_ascii=False, indent=4)
        print(f"✓ Saved {len(locations)} RAW locations to locations_raw.json")
        
        print("\n" + "="*60)
        print("RAW Data Sample (before cleaning):")
        print("="*60)
        print(df.head(10).to_string(index=False))
    else:
        print("\n⚠ No locations found")
    
    print("\n" + "="*60)
    print("✓ Scraping Complete!")
    print("="*60)