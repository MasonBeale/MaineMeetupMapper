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
        event_elements = driver.find_elements(By.CSS_SELECTOR, "article, div[class*='event'], div[class*='card']")
        
        print(f"✓ Found {len(event_elements)} potential event elements\n")
        
        seen_venues = set()
        
        # Extract text from each element
        for i, element in enumerate(event_elements):
            try:
                text = element.text
                
                if not text or len(text) < 10:
                    continue
                
                lines = text.split('\n')
                
                for j, line in enumerate(lines):
                    line = line.strip()
                    
                    if len(line) < 5:
                        continue
                    
                    # Skip obvious non-venue text
                    if re.search(r'^\w{3}\s+\d{1,2}', line):  # Date
                        continue
                    if re.search(r'^\d{1,2}:\d{2}', line):  # Time
                        continue
                    
                    # Look for address-like patterns
                    has_number = bool(re.search(r'\d', line))
                    has_letter = bool(re.search(r'[a-zA-Z]', line))
                    
                    if has_number and has_letter and len(line) > 10:
                        venue_name = "Unknown Venue"
                        address = line
                        city = "Portland"
                        zip_code = "04101"
                        
                        # Extract ZIP
                        zip_match = re.search(r'\b(\d{5})\b', line)
                        if zip_match:
                            zip_code = zip_match.group(1)
                        
                        # Parse venue name and address
                        if '•' in line:
                            parts = line.split('•')
                            if len(parts) >= 2:
                                venue_name = parts[0].strip()
                                address = parts[1].strip()
                        else:
                            if j > 0 and len(lines[j-1]) > 5 and not re.search(r'\d', lines[j-1]):
                                venue_name = lines[j-1].strip()
                        
                        # Parse city
                        if ',' in address:
                            addr_parts = address.split(',')
                            if len(addr_parts) >= 2:
                                address = addr_parts[0].strip()
                                city = addr_parts[1].strip()
                        
                        venue_key = f"{venue_name}_{address}"
                        
                        if venue_key not in seen_venues and address != "Unknown":
                            seen_venues.add(venue_key)
                            
                            location = {
                                'venue_name': venue_name,
                                'address': address,
                                'city': city,
                                'zip_code': zip_code
                            }
                            
                            locations.append(location)
                            print(f"{len(locations)}. {venue_name} - {city}, {zip_code}")
                            
                            if len(locations) >= 50:
                                break
                
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
        
        print("\n⚠ NOTE: This is RAW scraped data - contains junk entries")
        print("   Run 'python clean_data.py' next to clean the data")
    else:
        print("\n⚠ No locations found")
    
    print("\n" + "="*60)
    print("✓ Scraping Complete!")
    print("="*60)