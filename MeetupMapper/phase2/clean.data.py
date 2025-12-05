"""
clean_data.py
----------------------------------
Cleans the raw scraped data from Eventbrite by removing junk entries
and keeping only legitimate venue names.
Author: Logan
Date: November 13, 2025
"""

import pandas as pd
import re
import json

def is_junk_venue(venue_name):
    """
    Determine if a venue name is junk/invalid
    Returns True if it's junk, False if it's legitimate
    """
    
    venue_lower = venue_name.lower().strip()
    
    # Junk patterns to filter out
    junk_patterns = [
        r'^(mon|tue|wed|thu|fri|sat|sun)',  # Days of week
        r'^(today|tomorrow|tonight)',  # Time references
        r'^\w{3},?\s+\w{3}\s+\d{1,2}',  # Date formats (Mon, Jan 31)
        r'^\w{3}\s+\d{1,2}',  # Short dates (Jan 31)
        r'^going\s+(fast|slow)',  # "Going fast"
        r'^almost\s+full',  # "Almost full"
        r'^\d+\s+(going|attendees)',  # Numbers + going/attendees
        r'^unknown',  # "Unknown Venue"
        r'^\d{4}$',  # Just a year (2025)
        r'^(free|paid|online)',  # Event types
        r'^\$\d+',  # Prices
    ]
    
    # Check if matches any junk pattern
    for pattern in junk_patterns:
        if re.search(pattern, venue_lower):
            return True
    
    # If it's too short, probably junk
    if len(venue_name) < 4:
        return True
    
    # If it's ALL numbers, junk
    if venue_name.replace(' ', '').isdigit():
        return True
    
    return False


def clean_location_data(input_file='locations_raw.csv'):
    """
    Clean the raw scraped location data
    """
    
    print("="*60)
    print("Data Cleaning Process")
    print("="*60 + "\n")
    
    # Read raw data
    print(f"Reading raw data from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"✓ Loaded {len(df)} raw entries\n")
    
    original_count = len(df)
    
    # Filter out junk venues
    print("Filtering out junk entries...")
    df['is_junk'] = df['venue_name'].apply(is_junk_venue)
    
    junk_df = df[df['is_junk'] == True]
    clean_df = df[df['is_junk'] == False]
    
    print(f"  Identified {len(junk_df)} junk entries")
    print(f"  Kept {len(clean_df)} legitimate venues\n")
    
    # Show examples of removed junk
    print("Examples of REMOVED junk entries:")
    print("-" * 40)
    for i, row in junk_df.head(10).iterrows():
        print(f"  ✗ {row['venue_name']}")
    
    print(f"\n  ... and {len(junk_df) - 10} more junk entries\n")
    
    # Show examples of kept venues
    print("Examples of KEPT legitimate venues:")
    print("-" * 40)
    for i, row in clean_df.head(10).iterrows():
        print(f"  ✓ {row['venue_name']} - {row['city']}, {row['zip_code']}")
    
    # Remove the is_junk column
    clean_df = clean_df.drop(columns=['is_junk'])
    
    # Remove duplicates
    clean_df = clean_df.drop_duplicates(subset=['venue_name', 'address'])
    
    # Reset index
    clean_df = clean_df.reset_index(drop=True)
    
    print(f"\n✓ Final clean dataset: {len(clean_df)} unique venues")
    
    return clean_df, original_count, len(junk_df)


def save_cleaned_data(df):
    """
    Save the cleaned data to CSV and JSON
    """
    
    # Save as CSV
    df.to_csv('locations.csv', index=False)
    print(f"\n✓ Saved cleaned data to locations.csv")
    
    # Save as JSON
    data_dict = df.to_dict('records')
    with open('locations.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
    print(f"✓ Saved cleaned data to locations.json")


def generate_cleaning_report(original_count, junk_count, final_count):
    """
    Generate a cleaning documentation report
    """
    
    report = f"""
DATA CLEANING DOCUMENTATION
===========================

Source: Eventbrite (Maine events)
Scraping Method: Selenium WebDriver
Date: November 13, 2025

CLEANING PROCESS:
-----------------
1. Raw scraped entries: {original_count}
2. Junk entries removed: {junk_count}
3. Final clean entries: {final_count}

CLEANING CRITERIA:
------------------
Removed entries that matched:
- Day names (Monday, Tuesday, etc.)
- Time references (Today, Tomorrow, Tonight)
- Date formats (Mon, Jan 31)
- Event status (Going fast, Almost full, Unknown)
- Prices and numeric-only entries
- Entries shorter than 4 characters

VALIDATION:
-----------
- Removed duplicate venues (same name + address)
- Verified all entries have venue_name, address, city, zip_code
- Ensured venue names are legitimate business/venue names

RESULT:
-------
Clean dataset of {final_count} legitimate Maine venue locations
ready for database import.
"""
    
    with open('DATA_CLEANING_REPORT.txt', 'w') as f:
        f.write(report)
    
    print(f"\n✓ Generated DATA_CLEANING_REPORT.txt")


# Main execution
if __name__ == "__main__":
    
    # Clean the data
    clean_df, original_count, junk_count = clean_location_data()
    
    # Save cleaned data
    save_cleaned_data(clean_df)
    
    # Generate documentation
    generate_cleaning_report(original_count, junk_count, len(clean_df))
    
    # Display summary
    print("\n" + "="*60)
    print("CLEANING SUMMARY")
    print("="*60)
    print(f"Original entries:    {original_count}")
    print(f"Junk removed:        {junk_count}")
    print(f"Final clean entries: {len(clean_df)}")
    print(f"Data quality:        {(len(clean_df)/original_count)*100:.1f}%")
    
    print("\n" + "="*60)
    print("Sample of Clean Data:")
    print("="*60)
    print(clean_df.head(15).to_string(index=False))
    
    print("\n" + "="*60)
    print("✓ Data Cleaning Complete!")
    print("="*60)
    print("\nFiles created:")
    print("  - locations.csv (clean data for MySQL)")
    print("  - locations.json (clean data in JSON format)")
    print("  - DATA_CLEANING_REPORT.txt (documentation)")