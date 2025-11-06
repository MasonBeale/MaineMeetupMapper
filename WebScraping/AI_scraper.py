# pip install requests beautifulsoup4 selenium pandas lxml
# doesnt actually work but i wanted to see what i could get
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin, urlencode
import json

class MeetupScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.meetup.com"
        
    def search_events(self, location="New York", category="technology", count=20):
        """
        Search for events by location and category
        """
        params = {
            'location': location,
            'category': category,
            'source': 'EVENTS'
        }
        
        search_url = f"{self.base_url}/find/events/"
        events = []
        
        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            event_cards = soup.find_all('div', class_=lambda x: x and 'event-card' in x)
            
            for card in event_cards[:count]:
                event_data = self._parse_event_card(card)
                if event_data:
                    events.append(event_data)
                    
                
        except Exception as e:
            print(f"Error searching events: {e}")
            
        return events
    
    def _parse_event_card(self, card):
        """
        Parse individual event card
        """
        try:
            # Event title and link
            title_elem = card.find('h3') or card.find('h2') or card.find('a', {'aria-label': True})
            title = title_elem.get_text().strip() if title_elem else "N/A"
            
            link_elem = card.find('a', href=True)
            link = urljoin(self.base_url, link_elem['href']) if link_elem else "N/A"
            
            # Date and time
            date_elem = card.find('time')
            date = date_elem.get_text().strip() if date_elem else "N/A"
            
            # Location
            location_elem = card.find('span', string=re.compile(r'[A-Za-z\s,]+'))
            location = location_elem.get_text().strip() if location_elem else "N/A"
            
            # Group name
            group_elem = card.find('p', class_=lambda x: x and 'group-name' in x)
            group = group_elem.get_text().strip() if group_elem else "N/A"
            
            # Attendance
            attendees_elem = card.find('span', string=re.compile(r'\d+\s*(going|members)'))
            attendees = attendees_elem.get_text().strip() if attendees_elem else "N/A"
            
            return {
                'title': title,
                'date': date,
                'location': location,
                'group': group,
                'attendees': attendees,
                'link': link
            }
            
        except Exception as e:
            print(f"Error parsing event card: {e}")
            return None
    
    def get_event_details(self, event_url):
        """
        Get detailed information from individual event page
        """
        try:
            response = self.session.get(event_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract detailed information
            description_elem = soup.find('div', {'data-element-name': 'eventDescription'})
            description = description_elem.get_text().strip() if description_elem else "N/A"
            
            # Price information
            price_elem = soup.find('span', string=re.compile(r'\$|free|Free', re.I))
            price = price_elem.get_text().strip() if price_elem else "Free"
            
            return {
                'description': description[:500] + '...' if len(description) > 500 else description,
                'price': price
            }
            
        except Exception as e:
            print(f"Error getting event details: {e}")
            return {'description': 'N/A', 'price': 'N/A'}
    
    def scrape_events(self, locations=None, categories=None, max_events=50):
        """
        Main method to scrape events from multiple locations and categories
        """
        if locations is None:
            locations = ['New York', 'San Francisco', 'London']
        
        if categories is None:
            categories = ['technology', 'business', 'social']
        
        all_events = []
        
        for location in locations:
            for category in categories:
                print(f"Scraping {category} events in {location}...")
                
                events = self.search_events(location, category, count=15)
                
                # Get additional details for each event
                for event in events:
                    if event['link'] != "N/A":
                        details = self.get_event_details(event['link'])
                        event.update(details)
                        time.sleep(2)  # Be respectful
                    
                    all_events.append(event)
                    
                    if len(all_events) >= max_events:
                        break
                
                if len(all_events) >= max_events:
                    break
                time.sleep(3)
            
            if len(all_events) >= max_events:
                break
        
        return all_events[:max_events]
    
    def save_to_csv(self, events, filename='meetup_events.csv'):
        """
        Save events to CSV file
        """
        df = pd.DataFrame(events)
        df.to_csv(filename, index=False)
        print(f"Saved {len(events)} events to {filename}")
    
    def save_to_json(self, events, filename='meetup_events.json'):
        """
        Save events to JSON file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(events)} events to {filename}")

# Usage Example
def main():
    scraper = MeetupScraper()
    
    # Customize your search
    locations = ['New York', 'Chicago', 'Los Angeles']
    categories = ['technology', 'business', 'career']
    
    print("Starting Meetup.com scraping...")
    events = scraper.scrape_events(
        locations=locations,
        categories=categories,
        max_events=30
    )
    
    print(f"Scraped {len(events)} events")
    
    # Save results
    scraper.save_to_csv(events)
    scraper.save_to_json(events)
    
    # Display sample results
    for i, event in enumerate(events[:5], 1):
        print(f"\n--- Event {i} ---")
        print(f"Title: {event.get('title', 'N/A')}")
        print(f"Date: {event.get('date', 'N/A')}")
        print(f"Location: {event.get('location', 'N/A')}")
        print(f"Group: {event.get('group', 'N/A')}")
        print(f"Link: {event.get('link', 'N/A')}")

if __name__ == "__main__":
    main()