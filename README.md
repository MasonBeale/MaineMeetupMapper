# MaineMeetupMapper
## The Team:
Team Lead: Mason Beale | mason.beale@maine.edu

Kristina Zbinden | kristina.zbinden@maine.edu

Logan Simba | logan.simba@maine.edu

Phil Lane | philip.lane@maine.edu

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

3. Scraping of [https://www.visitmaine.com](https://www.visitmaine.com)

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

### Mason
1. Ownership of review & RSVP tables - CRUD and stored procedures for each
2. Scraping https://www.meetup.com/


### Phil
1. Ownership of Event Table -
   - CRUD procedures,
   - indexes,
   - and query examples

2. Scraping of https://www.mainepublic.org/
   - Script for scraping
   - Script for inserting data into SQL database
