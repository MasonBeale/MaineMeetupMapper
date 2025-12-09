# MaineMeetupMapper
## The Team:
Team Lead: Mason Beale | mason.beale@maine.edu | MasonBeale

Kristina Zbinden | kristina.zbinden@maine.edu | kristinazbinden

Logan Simba | logan.simba@maine.edu | LoganSimba

Phil Lane | philip.lane@maine.edu | phlane

# RUN/SETUP

## 1. Prerequisites
This application requires **MySQL 8.4** to be installed and running on your system.
Other versions may work but have **NOT** been tested.

### a. Install Dependencies
Before running the application, install all required Python dependencies:

```bash
pip install -r requirements.txt
```

### b. Configure Database Connection
Edit `Database_Startup/config.ini` with your MySQL credentials:

```ini
[database]
host = localhost
user = root
password = your_mysql_password
database_name = mmmdb
```

Update the `host`, `user`, `password`, and `database_name` fields to match your MySQL setup.

## 2. Getting Started

### a. Initialize the Database
Navigate to the `Database_Startup/` directory and run:

```bash
python startup.py
```
This script will:
- Create all necessary database tables
- Set up stored procedures
- Initialize the database schema

### b. Start the Application
From the project root directory, run:
```bash
python startup_site.py
```
This script will:
- Start the backend server
- Launch the frontend application
