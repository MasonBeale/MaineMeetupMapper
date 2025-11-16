# MaineMeetupMapper
## The Team:
Team Lead: Mason Beale | mason.beale@maine.edu

Kristina Zbinden | kristina.zbinden@maine.edu

Logan Simba | logan.simba@maine.edu

Phil Lane | philip.lane@maine.edu

# HOW TO RUN / SETUP
## 1. Run startup.py
This database system is intended to be run using MySQL84.

Run startup.py with the command line arguments: host, username, password, database name.

## 2. Run Web Scrapers
This project has multiple web scrapers that can be used to scrape data from different websites.

### Scraping of https://www.meetup.com/
Run meetup_scraper.py and events will be stored in meetup_events.json

### Scraping of [https://www.visitmaine.com](https://www.visitmaine.com)

#### To test scraper -
- Start venv with `source .venv/bin/activate`
- `cd` into `Webscraping` and run `maine_tourism_scraper.py`

#### To test tables - 
- Start MySQL local server
- In terminal, enter MySQL commands:
    1. `CREATE DATABASE mmmdb;`
    2. `USE mmmdb;`
    3. Create tables by running:
        - `source <your absolute path to MaineMeetupMapper/Tables/user_table.sql>;`
        - `source <your absolute path to MaineMeetupMapper/Tables/category_table.sql>;`
    4. Load procedures by running:
        - `source <your absolute path to MaineMeetupMapper/Procedures/user_procedures.sql>;`
        - `source <your absolute path to MaineMeetupMapper/Procedures/category_procedures.sql>;`
    5. Test procedures by running:
        - `source <your absolute path to MaineMeetupMapper/Test_Data/test_userdb.sql>;`
        - `source <your absolute path to MaineMeetupMapper/Test_Data/test_categorydb.sql>;`

### Scraping of https://www.mainepublic.org/

#### To test scraper -
- Start maine_public_scraper by command line or within IDE
- (As of now) Select whether you want to scrape the full event catalog, specific pages, or update since last use.
- View generated JSON file of events.

#### To test table - 
- After running startup.py
- Start and connect to MySQL local server
- If using MySQL Workbench, connect to database server (localhost)
- Test table by running
   - "select * from Event;"

## Phase 2
### Tasks, deadlines, and Main Contributors:
1. Recorded Video Demo (Nov, 13)
    * Mason
3. Database schema scripts (Nov, 7)
    * Phil
5. Stored procedures and functions (Nov, 10)
    * Kristina, Logan
6. Data scraping (Nov, 7)
    * Mason, Phil, Logan
7. Sample data and data cleaning (Nov, 8)
    * Mason, Phil, Logan
8. Query optimization analysis (Nov, 13)
    * Kristina
9. Readme (Nov, 14)
    * All
11. Team contributions (Nov, 14)
    * All

### Member ID's:
Mason : MasonBeale

Logan : LoganSimba

Phil : phlane

Kristina : kristinazbinden

## Team Contributions
### Kristina
1. Ownership of User Table
    - Create User Schema 
        - Create, Write, Update and Delete procedures
        - Create test cases

2. Ownership of Category Table
    - Create Category Schema 
        - Create, Write, Update and Delete procedures
        - Create test cases

### Mason
1. Ownership of review & RSVP tables
   - Creation of files
   - CRUD procedures
2. Scraping https://www.meetup.com/
   - scaping the website
   - loading information to a json
3. Creating the database startup script
4. Github Cleanup
   - trying to make everything consistent
   - putting everything into folders

### Phil
1. Ownership of Event Table -
   - CRUD procedures,
   - indexes,
   - and query examples

2. Scraping of https://www.mainepublic.org/
   - Script for scraping
   - Script for inserting data into SQL database
