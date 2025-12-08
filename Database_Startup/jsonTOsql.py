"""
This script receives a maine_events.json file and imports the data
into an SQL database.

Author: Philip Lane and Claude Sonnet 4.5
Date: 11/15/2025
"""

import json
import mysql.connector
from datetime import datetime
import sys


def connect_to_db():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if needed
            user='root',  # Change to your MySQL username
            password='password',  # Change to your MySQL password
            database='meetup_mapper'
        )
        print("✓ Connected to database successfully")
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to database: {e}")
        sys.exit(1)


def parse_date(date_string):
    """Convert MM-DD-YYYY to MySQL date format YYYY-MM-DD"""
    if not date_string:
        return None
    try:
        # Parse MM-DD-YYYY
        date_obj = datetime.strptime(date_string, '%m-%d-%Y')
        # Return in YYYY-MM-DD format
        return date_obj.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"  Warning: Could not parse date '{date_string}': {e}")
        return None


def parse_time(time_string):
    """Convert time string to MySQL time format HH:MM:SS"""
    if not time_string:
        return None
    try:
        # Parse "02:30 PM" format
        time_obj = datetime.strptime(time_string, '%I:%M %p')
        # Return in HH:MM:SS format
        return time_obj.strftime('%H:%M:%S')
    except Exception as e:
        print(f"  Warning: Could not parse time '{time_string}': {e}")
        return None


def get_or_create_location(cursor, venue_name, street, city, zip_code):
    """Get existing location_id or create new location, return location_id"""
    if not venue_name:
        return None

    try:
        # Check if location exists (match by venue_name and zip_code)
        query = """
                SELECT location_id \
                FROM location
                WHERE venue_name = %s \
                  AND COALESCE(zip_code, '') = COALESCE(%s, '') \
                """
        cursor.execute(query, (venue_name, zip_code))
        result = cursor.fetchone()

        if result:
            print(f"    ↪ Using existing location_id: {result[0]}")
            return result[0]

        # Location doesn't exist, create it
        insert_query = """
                       INSERT INTO location (venue_name, address, city, zip_code)
                       VALUES (%s, %s, %s, %s) \
                       """
        cursor.execute(insert_query, (venue_name, street, city, zip_code))
        location_id = cursor.lastrowid
        print(f"    ✓ Created new location_id: {location_id} for '{venue_name}'")
        return location_id

    except mysql.connector.Error as e:
        print(f"  Warning: Error handling location '{venue_name}': {e}")
        return None


def event_exists(cursor, event_name, event_date):
    """Check if event already exists in database"""
    query = """
            SELECT event_id \
            FROM event
            WHERE event_name = %s \
              AND event_date = %s \
            """
    cursor.execute(query, (event_name, event_date))
    return cursor.fetchone() is not None


def import_events(json_file, skip_duplicates=True):
    """Import events from JSON file to SQL database"""

    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        print(f"✓ Loaded {len(events)} events from {json_file}")
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON file: {e}")
        sys.exit(1)

    # Connect to database
    connection = connect_to_db()
    cursor = connection.cursor()

    # Statistics
    inserted = 0
    skipped = 0
    errors = 0

    print(f"\n📥 Starting import...")

    for i, event in enumerate(events, 1):
        try:
            # Extract and parse data
            event_name = event.get('title')
            event_date = parse_date(event.get('date'))
            start_time = parse_time(event.get('start_time'))
            end_time = parse_time(event.get('end_time'))

            # Get venue information
            venue_name = event.get('venue_name')
            street = event.get('street')
            city = event.get('city')
            zip_code = event.get('zip_code')

            # Validation
            if not event_name or not event_date:
                print(f"  [{i}/{len(events)}] ⚠️  Skipping event - missing name or date")
                skipped += 1
                continue

            # Check for duplicates
            if skip_duplicates and event_exists(cursor, event_name, event_date):
                print(f"  [{i}/{len(events)}] ⏭️  Skipping duplicate: {event_name}")
                skipped += 1
                continue

            # Get or create location (this adds to location table if new)
            location_id = get_or_create_location(cursor, venue_name, street, city, zip_code)

            # Insert event
            insert_query = """
                           INSERT INTO event (event_name, event_date, start_time, end_time, organizer_id, location_id)
                           VALUES (%s, %s, %s, %s, null, %s) \
                           """

            cursor.execute(insert_query, (
                event_name,
                event_date,
                start_time,
                end_time,
                location_id
            ))

            inserted += 1
            if inserted % 10 == 0:
                print(f"  [{i}/{len(events)}] ✓ Imported {inserted} events...")

        except mysql.connector.Error as e:
            print(f"  [{i}/{len(events)}] ❌ Error importing event '{event.get('title', 'Unknown')}': {e}")
            errors += 1
            continue
        except Exception as e:
            print(f"  [{i}/{len(events)}] ❌ Unexpected error: {e}")
            errors += 1
            continue

    # Commit changes
    connection.commit()

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"📊 Import Summary:")
    print(f"   Total events in file: {len(events)}")
    print(f"   ✓ Successfully imported: {inserted}")
    print(f"   ⏭️  Skipped (duplicates): {skipped}")
    print(f"   ❌ Errors: {errors}")
    print(f"{'=' * 60}\n")

    # Close connection
    cursor.close()
    connection.close()
    print("✓ Database connection closed")


if __name__ == "__main__":
    # Configuration
    JSON_FILE = 'maine_events.json'  # Your JSON file name
    SKIP_DUPLICATES = True  # Set to False to allow duplicate events

    import_events(JSON_FILE, skip_duplicates=SKIP_DUPLICATES)
