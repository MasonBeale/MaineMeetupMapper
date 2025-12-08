"""
Scrapes www.mainepublic.org for events and creates a JSON file
with event information.

Author: Philip Lane and Claude Sonnet 4.5
Date: 11/15/2025

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

        # Look for date pattern like "on Sat, 15 Nov 2025"
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


def parse_date_from_listing(item):
    """Extract date from the listing page PromoEvent-date element"""
    try:
        # Find the date element in the listing
        date_elem = item.find('p', class_='PromoEvent-date-date')
        if date_elem:
            # Text is like "Nov 15" or "Nov 15 Saturday"
            date_text = date_elem.text.strip()
            # Remove day of week if present
            date_text = re.sub(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', '', date_text).strip()

            # Parse "Nov 15" format
            parts = date_text.split()
            if len(parts) >= 2:
                month = parts[0]
                day = parts[1]

                # Get current year or next year
                current_month = datetime.now().month
                current_year = datetime.now().year

                month_map = {
                    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
                    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
                    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                }

                month_num = month_map.get(month, 1)

                # If event month is before current month, it's next year
                if month_num < current_month:
                    year = current_year + 1
                else:
                    year = current_year

                # Format as MM-DD-YYYY
                return f"{str(month_num).zfill(2)}-{day.zfill(2)}-{year}"

    except Exception as e:
        print(f"    Error parsing date from listing: {e}")

    return None


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


def parse_address(address_string):
    """Parse address string into components"""
    if not address_string:
        return None, None, None, None

    try:
        # Clean the address - replace newlines with commas
        address = address_string.strip().replace('\n', ', ')

        # Try to parse: "123 Main St, Portland, ME 04101"
        # Split by comma
        parts = [p.strip() for p in address.split(',') if p.strip()]

        street = None
        city = None
        state = None
        zip_code = None

        if len(parts) >= 1:
            street = parts[0]

        if len(parts) >= 2:
            # Check if second part contains state and zip
            second_part = parts[1].strip()
            # Look for state/zip pattern in second part
            state_zip_match = re.search(r'([A-Z]{2})\s*(\d{5}(?:-\d{4})?)', second_part)
            if state_zip_match:
                # Second part has state and zip, so no separate city
                state = state_zip_match.group(1)
                zip_code = state_zip_match.group(2)
                # Try to extract city from before the state
                city_part = re.sub(r'[A-Z]{2}\s*\d{5}(?:-\d{4})?', '', second_part).strip()
                if city_part:
                    city = city_part
            else:
                # Second part is likely city
                city = second_part

        if len(parts) >= 3:
            # Third part usually contains state and/or zip
            last_part = parts[2].strip()

            # Try to extract state (2 letters) and zip (5 digits or 5+4)
            match = re.search(r'([A-Z]{2})\s*(\d{5}(?:-\d{4})?)', last_part)
            if match:
                if not state:  # Only set if not already set
                    state = match.group(1)
                if not zip_code:  # Only set if not already set
                    zip_code = match.group(2)
            else:
                # Try just zip code
                zip_match = re.search(r'(\d{5}(?:-\d{4})?)', last_part)
                if zip_match and not zip_code:
                    zip_code = zip_match.group(1)

                # Try just state
                state_match = re.search(r'\b([A-Z]{2})\b', last_part)
                if state_match and not state:
                    state = state_match.group(1)

        # If we still don't have state but have a part that looks like a state name
        if not state:
            for part in parts:
                if part.strip() in ['Maine', 'ME']:
                    state = 'ME'
                    break

        return street, city, state, zip_code

    except Exception as e:
        print(f"Error parsing address '{address_string}': {e}")
        return None, None, None, None


def scrape_event_details(event_url):
    """Scrape individual event page for location details"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(event_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        location_data = {
            'venue_name': None,
            'street': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'phone': None,
            'email': None,
            'website': None
        }

        # Find venue information section
        venue_info = soup.find('div', class_='VenueInformation')

        if venue_info:
            # Extract venue name - try multiple possible locations
            venue_name_elem = venue_info.find('span', class_='VenueInformation-text-name')
            if not venue_name_elem:
                # Try alternate location
                venue_name_elem = venue_info.find('div', class_='VenueInformation-text')
                if venue_name_elem:
                    name_span = venue_name_elem.find('span')
                    if name_span:
                        venue_name_elem = name_span

            if venue_name_elem:
                location_data['venue_name'] = venue_name_elem.text.strip()

            # Extract address components directly from specific elements
            street_elem = venue_info.find('span', class_='VenueInformation-address-street')
            city_elem = venue_info.find('span', class_='VenueInformation-address-city')
            state_elem = venue_info.find('span', class_='VenueInformation-address-state')
            zip_elem = venue_info.find('span', class_='VenueInformation-address-zip')

            if street_elem:
                location_data['street'] = street_elem.text.strip()
            if city_elem:
                location_data['city'] = city_elem.text.strip()
            if state_elem:
                location_data['state'] = state_elem.text.strip()
            if zip_elem:
                location_data['zip_code'] = zip_elem.text.strip()

            # Fallback: if we didn't get address from spans, try the full address div
            if not location_data['street']:
                address_elem = venue_info.find('div', class_='VenueInformation-address')
                if address_elem:
                    address_text = address_elem.text.strip()
                    street, city, state, zip_code = parse_address(address_text)
                    location_data['street'] = street or location_data['street']
                    location_data['city'] = city or location_data['city']
                    location_data['state'] = state or location_data['state']
                    location_data['zip_code'] = zip_code or location_data['zip_code']

            # Extract phone
            phone_elem = venue_info.find('div', class_='VenueInformation-phone')
            if phone_elem:
                location_data['phone'] = phone_elem.text.strip()

            # Extract email
            email_elem = venue_info.find('div', class_='VenueInformation-email')
            if email_elem:
                location_data['email'] = email_elem.text.strip()

            # Extract website
            website_elem = venue_info.find('div', class_='VenueInformation-website')
            if website_elem:
                link = website_elem.find('a')
                if link and link.get('href'):
                    location_data['website'] = link['href']

        # If venue_name is still None, try to get from the event page content
        if not location_data['venue_name']:
            # Try EventPage-venueInformation
            venue_section = soup.find('div', class_='EventPage-venueInformation')
            if venue_section:
                venue_text = venue_section.find('div', class_='VenueInformation-text')
                if venue_text:
                    location_data['venue_name'] = venue_text.text.strip().split('\n')[0].strip()

        return location_data

    except Exception as e:
        print(f"Error scraping event details from {event_url}: {e}")
        return None
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


def scrape_event_listing(url, scrape_details=True):
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

        print(f"    Found {len(event_items)} items on page")

        for item in event_items:
            try:
                # Find the PromoEvent element within the li
                promo_event = item.find('ps-promo', class_='PromoEvent')
                if not promo_event:
                    continue

                # Extract title
                title_elem = promo_event.find('h3', class_='PromoEvent-title')
                if title_elem:
                    title_link = title_elem.find('a')
                    title = title_link.text.strip() if title_link else title_elem.text.strip()
                else:
                    title = None

                # Get event link
                link_elem = promo_event.find('a', class_='PromoEvent-link-link')
                event_url = link_elem['href'] if link_elem else None
                if event_url and not event_url.startswith('http'):
                    event_url = 'https://www.mainepublic.org' + event_url

                # Extract description
                desc_elem = promo_event.find('div', class_='PromoEvent-description')
                desc = desc_elem.text.strip() if desc_elem else None

                # Extract time info from listing
                time_elem = promo_event.find('div', class_='PromoEvent-time')
                start_time, end_time, event_type, frequency_notes = parse_time_info(time_elem)

                # Extract date - first try from listing page, then from time element
                date = parse_date_from_listing(promo_event)
                if not date and time_elem:
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
                    'venue_name': None,
                    'street': None,
                    'city': None,
                    'state': None,
                    'zip_code': None,
                    'phone': None,
                    'email': None,
                    'website': None,
                }

                # Scrape location details from event page (always enabled now)
                if event_url:
                    try:
                        location_data = scrape_event_details(event_url)
                        if location_data:
                            event_data.update(location_data)
                        time.sleep(0.2)  # Small delay after scraping event page
                    except Exception as e:
                        print(f"    Error getting location for {title}: {e}")

                # Check for duplicates using unique key
                event_key = create_event_key(event_data)
                if event_key not in seen_keys:
                    seen_keys.add(event_key)
                    events.append(event_data)

            except Exception as e:
                print(f"    Error parsing event: {e}")
                continue

        return events
    except Exception as e:
        print(f"    Error scraping page {url}: {e}")
        return []


def scrape_page_batch(base_url, page_numbers, scrape_details=True):
    """Scrape a batch of pages and return results"""
    results = {}
    for page_num in page_numbers:
        print(f"  Worker processing page {page_num}...")
        # Correct URL format: ?f0=&from=&to=&q=&p=2
        if page_num == 1:
            url = base_url
        else:
            # Replace or add the p parameter
            if '?' in base_url:
                url = f"{base_url}&p={page_num}"
            else:
                url = f"{base_url}?p={page_num}"

        events = scrape_event_listing(url, scrape_details=scrape_details)
        results[page_num] = events
        print(f"  Page {page_num} complete: {len(events)} events")
        time.sleep(0.05)  # Tiny delay between pages in same worker
    return results


def calculate_optimal_workers(num_pages):
    """Calculate optimal batch size and worker count based on number of pages"""
    import os

    # Get CPU count (default to 8 if can't determine)
    cpu_count = os.cpu_count() or 8

    if num_pages <= 5:
        # Small job: 1 page per worker
        workers = min(num_pages, cpu_count)
        batch_size = 1
    elif num_pages <= 20:
        # Small-medium: 2 pages per worker
        workers = min(cpu_count, num_pages // 2 + 1)
        batch_size = 2
    elif num_pages <= 50:
        # Medium: use more workers, 3-5 pages per worker
        workers = min(cpu_count, 10)
        batch_size = max(3, num_pages // workers)
    else:
        # Large job: maximize parallelism
        workers = min(cpu_count, 12)  # Cap at 12 workers
        batch_size = max(5, num_pages // workers)

    return batch_size, workers


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
    if os.path.exists('./maine_events.json'):
        with open('./maine_events.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def scrape_pages_concurrent(base_url, start_page, end_page, scrape_details=True):
    """Scrape pages concurrently with dynamic worker allocation"""
    all_events = []
    seen_event_keys = set()  # Track duplicates across all pages

    num_pages = end_page - start_page + 1
    batch_size, max_workers = calculate_optimal_workers(num_pages)

    # Create batches of pages
    page_batches = []
    for i in range(start_page, end_page + 1, batch_size):
        batch = list(range(i, min(i + batch_size, end_page + 1)))
        page_batches.append(batch)

    detail_status = "with location details" if scrape_details else "without location details"
    print(f"\n Scraping Strategy:")
    print(f"   Pages: {num_pages}")
    print(f"   Workers: {max_workers}")
    print(f"   Batch size: {batch_size} pages/worker")
    print(f"   Total batches: {len(page_batches)}")
    print(f"   Mode: {detail_status}\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all batches
        future_to_batch = {
            executor.submit(scrape_page_batch, base_url, batch, scrape_details): batch
            for batch in page_batches
        }

        # Process completed batches
        completed = 0
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            completed += 1

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
                    duplicates = len(events) - len(unique_events)
                    print(f"✓ Page {page_num}: {len(unique_events)} unique events" +
                          (f" ({duplicates} duplicates filtered)" if duplicates > 0 else ""))

                    # Save progress periodically
                    if unique_events:
                        save_progress(page_num, unique_events[-1]['url'])

                print(f"Batch {completed}/{len(page_batches)} complete\n")

            except Exception as e:
                print(f"Error processing batch {batch}: {e}\n")

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


def save_to_json(events, filename='./maine_events.json', append_mode=False):
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
        print("\n Starting full scrape with concurrent processing...")
        print("  With location scraping enabled, this will take 30-60 minutes")

        # Full scrape
        events = scrape_pages_concurrent(base_url, 1, 400, scrape_details=True)
        save_to_json(events, append_mode=False)

    elif choice == '2':
        num_pages = input("How many pages to scrape? ").strip()
        try:
            num_pages = int(num_pages)
            print(f"\n Starting scrape of {num_pages} pages...")
            events = scrape_pages_concurrent(base_url, 1, num_pages, scrape_details=True)
            save_to_json(events, append_mode=False)
        except ValueError:
            print("Invalid number. Exiting.")
            exit(1)

    elif choice == '3':
        print("\n Starting update scrape...")
        events = scrape_with_update_mode(base_url, max_workers=5)
        save_to_json(events, append_mode=True)

    else:
        print("Invalid choice. Exiting.")
        exit(1)


    print(f"\n Scraping complete! Total new events: {len(events)}")
