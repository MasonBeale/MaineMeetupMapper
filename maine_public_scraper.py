"""
maine_public_scraper.py
---

This script scrapes www.mainepublic.org for all
events, a specific number of pages of events, or
updates or retrieves new events based on the last time
it was run.

Author: Phil Lane and Claude Sonnet 4.5
Date: 11/12/2025
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_date_from_time_element(time_elem):
    """Extract date from PromoEvent-time element (format: MM-DD-YYYY)"""
    if not time_elem:
        return None

    try:
        time_text = time_elem.text.strip()

        # Look for date pattern like "on Mon, 17 Nov 2025"
        date_match = re.search(r'on\s+\w+,\s+(\d{1,2})\s+(\w+)\s+(\d{4})', time_text)
        if date_match:
            day = date_match.group(1)
            month = date_match.group(2)
            year = date_match.group(3)

            # Convert month name to number
            month_map = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }

            month_num = month_map.get(month, '01')

            # Format as MM-DD-YYYY (US format)
            return f"{month_num}-{day.zfill(2)}-{year}"

        # If no explicit date, try to extract from context
        # Look for standalone date patterns
        alt_date_match = re.search(r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', time_text)
        if alt_date_match:
            month = alt_date_match.group(1)
            day = alt_date_match.group(2)
            year = alt_date_match.group(3)

            month_map = {
                'January': '01', 'February': '02', 'March': '03', 'April': '04',
                'May': '05', 'June': '06', 'July': '07', 'August': '08',
                'September': '09', 'October': '10', 'November': '11', 'December': '12',
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09',
                'Oct': '10', 'Nov': '11', 'Dec': '12'
            }

            month_num = month_map.get(month, '01')
            return f"{month_num}-{day.zfill(2)}-{year}"

    except Exception as e:
        print(f"Error parsing date from time element: {e}")

    return None


def parse_time_info(time_elem):
    """Parse time element to extract clean start/end times and event type"""
    if not time_elem:
        return None, None, "single", None

    time_text = time_elem.text.strip()
    event_type = "single"
    frequency_notes = None
    start_time = None
    end_time = None

    # Check for recurring patterns
    if "every" in time_text.lower() or "weekly" in time_text.lower():
        event_type = "recurring"

        # Extract frequency information
        if "every" in time_text.lower():
            frequency_match = re.search(r'Every\s+(\d+\s+weeks?)[^.]*', time_text, re.IGNORECASE)
            if frequency_match:
                frequency_notes = frequency_match.group(0)

        # Extract day of week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            if day in time_text:
                if frequency_notes:
                    frequency_notes += f" on {day}"
                else:
                    frequency_notes = f"Weekly on {day}"
                break

    # Extract times using regex
    time_pattern = r'(\d{1,2}:\d{2}\s*[AP]M)'
    times = re.findall(time_pattern, time_text, re.IGNORECASE)

    if len(times) >= 1:
        start_time = times[0].upper().strip()
    if len(times) >= 2:
        end_time = times[1].upper().strip()

    return start_time, end_time, event_type, frequency_notes


def is_past_event(date_str):
    """Check if an event date has already passed"""
    if not date_str:
        return False

    try:
        # Parse MM-DD-YYYY format
        event_date = datetime.strptime(date_str, '%m-%d-%Y')
        current_date = datetime.now()

        # Return True if event is in the past
        return event_date.date() < current_date.date()
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        return False


def create_event_key(event):
    """Create a unique key for an event to detect duplicates"""
    # Use URL as primary key since it's unique per event
    if event.get('url'):
        return event['url']

    # Fallback: use combination of title, date, and start_time
    title = event.get('title', '').strip().lower()
    date = event.get('date', '')
    start_time = event.get('start_time', '')

    return f"{title}|{date}|{start_time}"


def scrape_event_listing(url):
    """Scrape the main calendar listing page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        events = []
        seen_keys = set()  # Track duplicates within the same page

        # Find all event items
        event_items = soup.find_all('li', class_='EventSearchResultsModule-results-item')

        for item in event_items:
            try:
                # Extract title
                title_elem = item.find('h3', class_='PromoEvent-title')
                title = title_elem.text.strip() if title_elem else None

                # Get event link
                link_elem = item.find('a', class_='PromoEvent-link-link')
                event_url = link_elem['href'] if link_elem else None
                if event_url and not event_url.startswith('http'):
                    event_url = 'https://www.mainepublic.org' + event_url

                # Extract description
                desc_elem = item.find('div', class_='PromoEvent-description')
                desc = desc_elem.text.strip() if desc_elem else None

                # Extract time info from listing
                time_elem = item.find('div', class_='PromoEvent-time')
                start_time, end_time, event_type, frequency_notes = parse_time_info(time_elem)

                # Extract date from time element
                date = parse_date_from_time_element(time_elem)

                # Skip past events
                if date and is_past_event(date):
                    continue

                event_data = {
                    'title': title,
                    'desc': desc,
                    'date': date,
                    'start_time': start_time,
                    'end_time': end_time,
                    'event_type': event_type,
                    'frequency_notes': frequency_notes,
                    'url': event_url,
                    'max_capacity': None,
                    'attendees': None
                }

                # Check for duplicates using unique key
                event_key = create_event_key(event_data)
                if event_key not in seen_keys:
                    seen_keys.add(event_key)
                    events.append(event_data)

            except Exception as e:
                print(f"Error parsing event: {e}")
                continue

        return events
    except Exception as e:
        print(f"Error scraping page {url}: {e}")
        return []


def scrape_page_batch(base_url, page_numbers):
    """Scrape a batch of pages and return results"""
    results = {}
    for page_num in page_numbers:
        # Correct URL format: ?f0=&from=&to=&q=&p=2
        if page_num == 1:
            url = base_url
        else:
            # Replace or add the p parameter
            if '?' in base_url:
                url = f"{base_url}&p={page_num}"
            else:
                url = f"{base_url}?p={page_num}"

        events = scrape_event_listing(url)
        results[page_num] = events
        time.sleep(0.1)  # Small delay between requests in same thread
    return results


def load_progress():
    """Load scraping progress from file"""
    if os.path.exists('scraper_progress.json'):
        with open('scraper_progress.json', 'r') as f:
            return json.load(f)
    return {'last_page': 0, 'last_event_url': None, 'last_run': None}


def save_progress(page, last_event_url):
    """Save scraping progress"""
    progress = {
        'last_page': page,
        'last_event_url': last_event_url,
        'last_run': datetime.now().isoformat()
    }
    with open('scraper_progress.json', 'w') as f:
        json.dump(progress, f, indent=2)


def load_existing_events():
    """Load existing events from main file"""
    if os.path.exists('maine_events.json'):
        with open('maine_events.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def scrape_pages_concurrent(base_url, start_page, end_page, batch_size=10, max_workers=5):
    """Scrape pages concurrently in batches"""
    all_events = []
    seen_event_keys = set()  # Track duplicates across all pages

    # Create batches of pages
    page_batches = []
    for i in range(start_page, end_page + 1, batch_size):
        batch = list(range(i, min(i + batch_size, end_page + 1)))
        page_batches.append(batch)

    print(f"Scraping {end_page - start_page + 1} pages in {len(page_batches)} batches using {max_workers} workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all batches
        future_to_batch = {
            executor.submit(scrape_page_batch, base_url, batch): batch
            for batch in page_batches
        }

        # Process completed batches
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                results = future.result()
                # Sort by page number and add events
                for page_num in sorted(results.keys()):
                    events = results[page_num]

                    # Filter duplicates across pages
                    unique_events = []
                    for event in events:
                        event_key = create_event_key(event)
                        if event_key not in seen_event_keys:
                            seen_event_keys.add(event_key)
                            unique_events.append(event)

                    all_events.extend(unique_events)
                    print(
                        f"Page {page_num}: Found {len(events)} events ({len(unique_events)} unique, {len(events) - len(unique_events)} duplicates)")

                    # Save progress periodically
                    if unique_events:
                        save_progress(page_num, unique_events[-1]['url'])

            except Exception as e:
                print(f"Error processing batch {batch}: {e}")

    return all_events


def scrape_with_update_mode(base_url, max_workers=5):
    """Scrape pages until we hit existing content"""
    existing_events = load_existing_events()
    existing_urls = {event['url'] for event in existing_events if event.get('url')}
    print(f"Update mode: Found {len(existing_urls)} existing events")

    all_new_events = []
    seen_event_keys = set()  # Track duplicates
    page = 1
    consecutive_duplicates = 0

    while consecutive_duplicates < 20:
        print(f"\nChecking pages {page} to {page + 9}...")

        # Scrape 10 pages at a time
        events_batch = scrape_pages_concurrent(base_url, page, page + 9, batch_size=2, max_workers=max_workers)

        if not events_batch:
            print("No more events found.")
            break

        # Check for duplicates
        new_events = []
        for event in events_batch:
            event_key = create_event_key(event)

            if event['url'] in existing_urls or event_key in seen_event_keys:
                consecutive_duplicates += 1
            else:
                seen_event_keys.add(event_key)
                new_events.append(event)
                consecutive_duplicates = 0

        all_new_events.extend(new_events)
        print(f"Found {len(new_events)} new events in this batch")

        if consecutive_duplicates >= 20:
            print(f"\nFound 20 consecutive existing events. Stopping update.")
            break

        page += 10

    return all_new_events


def save_to_json(events, filename='maine_events.json', append_mode=False):
    """Save events to JSON file"""
    if append_mode and os.path.exists(filename):
        existing_events = load_existing_events()
        existing_urls = {event['url'] for event in existing_events}

        # Add only new events
        for event in events:
            if event['url'] not in existing_urls:
                existing_events.append(event)

        events = existing_events

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(events)} total events to {filename}")


if __name__ == "__main__":
    base_url = "https://www.mainepublic.org/community-calendar?f0=&from=&to=&q="

    progress = load_progress()

    print("=" * 60)
    print("Maine Public Calendar Scraper (Concurrent Edition)")
    print("=" * 60)

    if progress['last_run']:
        print(f"\nLast run: {progress['last_run']}")
        print(f"Last page scraped: {progress['last_page']}")

    print("\nSelect scraping mode:")
    print("1. Full scrape (all pages)")
    print("2. Scrape specific number of pages")
    print("3. Update mode (scrape until existing content found)")

    choice = input("\nEnter your choice [1/2/3]: ").strip()

    if choice == '1':
        print("\n🚀 Starting full scrape with concurrent processing...")
        print("Estimated time: ~10-15 minutes for 395 pages")

        # Full scrape - we'll try to estimate total pages
        # Let's start with a reasonable estimate (395 pages)
        events = scrape_pages_concurrent(base_url, 1, 400, batch_size=10, max_workers=5)
        save_to_json(events, append_mode=False)

    elif choice == '2':
        num_pages = input("How many pages to scrape? ").strip()
        try:
            num_pages = int(num_pages)
            print(f"\n🚀 Starting scrape of {num_pages} pages with concurrent processing...")
            events = scrape_pages_concurrent(base_url, 1, num_pages, batch_size=10, max_workers=5)
            save_to_json(events, append_mode=False)
        except ValueError:
            print("Invalid number. Exiting.")
            exit(1)

    elif choice == '3':
        print("\n🔄 Starting update scrape...")
        events = scrape_with_update_mode(base_url, max_workers=5)
        save_to_json(events, append_mode=True)

    else:
        print("Invalid choice. Exiting.")
        exit(1)

    print(f"\n✅ Scraping complete! Total new events: {len(events)}")