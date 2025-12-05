# Location Data - Meetup Mapper Phase 2
**Author:** Logan  
**Date:** November 13, 2025

## Overview
This module handles location/venue data for the Meetup Mapper system, scraped from Eventbrite.

## Files
- `eventbrite_scraper.py` - Selenium-based scraper for Eventbrite
- `clean_data.py` - Data cleaning script
- `locations.csv` - Clean location data (23 venues)
- `locations_raw.csv` - Raw scraped data (50 entries)
- `DATA_CLEANING_REPORT.txt` - Cleaning documentation
- `create_location.sql` - Database table creation
- `location_procedures.sql` - Stored procedures

## How to Run

### 1. Web Scraping
```bash
pip install selenium webdriver-manager pandas
python eventbrite_scraper.py
python clean_data.py
```

### 2. Database Setup
```sql
-- In MySQL:
CREATE DATABASE meetup_mapper;
USE meetup_mapper;

-- Run SQL files in order:
source create_location.sql;
source location_procedures.sql;
```

## Data Source
- Website: https://www.eventbrite.com
- Location: Maine events
- Method: Selenium WebDriver
- Records: 23 clean venues (from 50 raw entries)