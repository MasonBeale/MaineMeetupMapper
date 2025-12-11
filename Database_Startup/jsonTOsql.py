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
from pathlib import Path
import argparse

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    base_dir = Path(__file__).parent
    possible_paths = [
        Path(config_file),
        base_dir / config_file,
        base_dir.parent / config_file,
        Path.cwd() / config_file,
    ]

    found = None
    for path in possible_paths:
        if Path(path).exists():
            config.read(path)
            if 'database' in config:
                found = path
                break

    if not found:
        raise FileNotFoundError(
            "Could not find a valid config.ini with a [database] section. "
            f"Searched: {', '.join(str(p) for p in possible_paths)}"
        )

    host = config.get('database', 'host', fallback='localhost')
    user = config.get('database', 'user', fallback='root')
    password = config.get('database', 'password', fallback=None)
    database_name = config.get('database', 'database_name', fallback='mmmdb')

    if not password:
        raise ValueError(
            "Missing database configuration in config.ini. Ensure 'password' is set under the [database] section."
        )

    return {
        'host': host,
        'user': user,
        'password': password,
        'database': database_name,
    }
config = load_config()

def parse_args():
    """Parse command-line arguments for database connection"""
    parser = argparse.ArgumentParser(description='Import JSON events to SQL database')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--user', default='root', help='Database user')
    parser.add_argument('--password', required=True, help='Database password')
    parser.add_argument('--database', default='mmmdb', help='Database name')
    return parser.parse_args()


def connect_to_db(host, user, password, database):
    """Connect to MySQL database using provided credentials"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # print(f"Connected to database: {database}")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
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
        # print(f"  Warning: Could not parse date '{date_string}': {e}")
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
        # print(f"  Warning: Could not parse time '{time_string}': {e}")
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
            # print(f"Using existing location_id: {result[0]}")
            return result[0]

        # Location doesn't exist, create it
        insert_query = """
                       INSERT INTO location (venue_name, address, city, zip_code)
                       VALUES (%s, %s, %s, %s) \
                       """
        cursor.execute(insert_query, (venue_name, street, city, zip_code))
        location_id = cursor.lastrowid
        # print(f"Created new location_id: {location_id} for '{venue_name}'")
        return location_id

    except mysql.connector.Error as e:
        # print(f"  Warning: Error handling location '{venue_name}': {e}")
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


def import_events(json_file, host, user, password, database, skip_duplicates=True):

    # Resolve JSON file path - search multiple locations
    json_path = None
    search_paths = [
        Path(json_file),                           # exact path provided
        Path(__file__).parent / json_file,         # same directory as script
        Path(__file__).parent.parent / json_file,  # parent directory (repo root)
        Path.cwd() / json_file,                    # current working directory
    ]
    
    for path in search_paths:
        if path.exists():
            json_path = path
            # print(f"Found JSON file at: {json_path}")
            break
    
    if not json_path:
        print(f"Error: File '{json_file}' not found in any of:")
        for path in search_paths:
            print(f"   - {path}")
        sys.exit(1)

    # Load JSON data
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            events = json.load(f)
        # print(f"Loaded {len(events)} events from {json_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)

    # Connect to database
    connection = connect_to_db(host, user, password, database)
    cursor = connection.cursor()

    # Statistics
    inserted = 0
    skipped = 0
    errors = 0

    print(f"Starting import...")

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
                # print(f"  [{i}/{len(events)}] Skipping event - missing name or date")
                skipped += 1
                continue

            # Check for duplicates
            if skip_duplicates and event_exists(cursor, event_name, event_date):
                # print(f"  [{i}/{len(events)}] Skipping duplicate: {event_name}")
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
                # print(f"  [{i}/{len(events)}]  Imported {inserted} events...")
                pass

        except mysql.connector.Error as e:
            # print(f"  [{i}/{len(events)}]  Error importing event '{event.get('title', 'Unknown')}': {e}")
            errors += 1
            continue
        except Exception as e:
            print(f"  [{i}/{len(events)}]  Unexpected error: {e}")
            errors += 1
            continue

    # Commit changes
    connection.commit()

    # Print summary
    print(f"{'=' * 60}")
    print(f"Import Summary:")
    print(f"Total events in file: {len(events)}")
    print(f"Successfully imported: {inserted}")
    print(f"Skipped (duplicates): {skipped}")
    print(f"Errors: {errors}")
    print(f"{'=' * 60}")

    # Close connection
    cursor.close()
    connection.close()
    # print(" Database connection closed")


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()
    
    # Configuration
    JSON_FILE = './maine_events.json'  # Your JSON file name
    SKIP_DUPLICATES = True  # Set to False to allow duplicate events

    import_events(
        JSON_FILE,
        host= config["host"],
        user= config["user"],
        password= config["password"],
        database= config["database"],
        skip_duplicates=SKIP_DUPLICATES
    )
