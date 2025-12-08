'''
startup.py
Initializes the database by creating necessary tables and stored procedures.
Then runs the Maine Public scraper and imports the data into the database.
Uses config.ini file for database connection parameters.
@author Mason Beale
'''
import sys
import subprocess
from pathlib import Path
import mysql.connector
import configparser
import json

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()

    # Look for config.ini in several sensible locations (cwd, script dir, parent)
    base_dir = Path(__file__).parent
    possible_paths = [
        Path(config_file),                    # relative to current working directory
        base_dir / config_file,               # same directory as this script
        base_dir.parent / config_file,        # parent directory
        Path.cwd() / config_file,             # explicit current working directory
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

def find_sql_files(directory):
    sql_files = []
    root_path = Path(directory)
    for sql_file in root_path.rglob("*.sql"):
        sql_files.append(sql_file)
    return sql_files

def execute_sql_files(files, cursor):
    for file in files:
        file = Path(file)
        if not file.exists():
            raise FileNotFoundError(f"SQL file not found: {file}")

        with open(file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        try:
            cursor.execute(sql_script)
        except Exception as e:
            raise RuntimeError(f"Error executing SQL file {file}: {e}")

def run_maine_public_scraper():
    
    scraper_file = Path(__file__).parent / 'maine_public_scraper.py'
    
    if not scraper_file.exists():
        print(f"Scraper file not found: {scraper_file}")
        print("Please ensure maine_public_scraper.py exists in the same directory.")
        return False
    
    try:
        print("Running scraper...")
        
        # Run the scraper as a subprocess
        result = subprocess.run(
            [sys.executable, str(scraper_file)],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Scraper stderr:", result.stderr)
        
        if result.returncode == 0:
            print("Maine Public scraper completed successfully!")
            return True
        else:
            print(f"Maine Public scraper failed with exit code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"Error running scraper: {e}")
        return False

def run_json_to_sql_importer(db_config):
    
    importer_file = Path(__file__).parent / 'jsonTOsql.py'
    json_file = Path(__file__).parent / 'maine_events.json'
    
    if not importer_file.exists():
        print(f"Importer file not found: {importer_file}")
        print("Please ensure jsonTOsql.py is in the same directory.")
        return False
    
    if not json_file.exists():
        print(f"JSON file not found: {json_file}")
        print("Please run the scraper first to generate maine_events.json")
        return False
    
    # Count events in JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        print(f"Found {len(events)} events in JSON file")
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return False
    
    try:
        print("Running JSON to SQL importer...")
        result = subprocess.run(
            [
                sys.executable,
                str(importer_file),
                '--host', db_config['host'],
                '--user', db_config['user'],
                '--password', db_config['password'],
                '--database', db_config['database']
            ],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Importer stderr:", result.stderr)
        
        if result.returncode == 0:
            print("JSON to SQL import completed successfully!")
            return True
        else:
            print(f"JSON to SQL import failed with exit code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"Error running importer: {e}")
        return False

def setup_database():
    
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config file: {e}")
        print("Make sure config.ini exists with proper database configuration")
        return False, None
    
    # Connect to MySQL server
    try:
        mydb = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        mycursor = mydb.cursor()
        
        # Create database if it doesn't exist
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config['database']}`")
        
        # Connect to the specific database
        mydb = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        mycursor = mydb.cursor()
        
        print(f"Successfully connected to database: {config['database']}")
        
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return False, None
    
    # Execute table creation scripts (use script directory as base)
    base_dir = Path(__file__).parent
    table_dir = base_dir / 'tables_'
    table_files = [
        table_dir / 'location_table.sql',
        table_dir / 'User_Table.sql',
        table_dir / 'event_table.sql',
        table_dir / 'Category_Table.sql',
        table_dir / 'review_table.sql',
        table_dir / 'RSVP_table.sql',
    ]

    print("Creating tables...")
    for file in table_files:
        if not file.exists():
            print(f"Table SQL file not found: {file}")
            return False, None
    
    execute_sql_files(table_files, mycursor)
    
    # Execute stored procedure scripts
    print("Creating stored procedures...")
    procedure_files = find_sql_files(str(base_dir / 'procedures_/'))
    if not procedure_files:
        print("No stored procedure files found in procedures_/ directory")
    else:
        execute_sql_files(procedure_files, mycursor)
    
    # Commit changes
    mydb.commit()
    print("Database initialization completed successfully!")
    
    # Close connections
    mycursor.close()
    mydb.close()
    
    return True, config

def main():
    success, config = setup_database()
    if not success:
        print("❌ Database setup failed. Exiting.")
        sys.exit(1)
    
    # Ask user if they want to run the scraper
    print("\n" + "="*60)
    print("Scraper and Importer Options")
    print("="*60)
    print("1. Run scraper and import data (full process)")
    print("2. Skip scraper, import existing JSON data only")
    print("3. Exit (database only setup)")
    
    choice = input("\nEnter your choice [1/2/3]: ").strip()
    
    if choice == '1':
        # Step 2: Run scraper
        if not run_maine_public_scraper():
            print("Scraper failed. Trying to import existing data if available...")
        
        # Step 3: Run importer
        if not run_json_to_sql_importer(config):
            print("Import failed, but database is ready")
    
    elif choice == '2':
        # Just run the importer with existing data
        if not run_json_to_sql_importer(config):
            print("Import failed, but database is ready")
    
    elif choice == '3':
        print("Database setup complete. Exiting.")
    
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("Summary:")
    print("- Database initialized with tables and procedures")
    print("- Maine Public events scraped (if selected)")
    print("- Data imported into SQL database (if selected)")
    print("\nYou can now run your Meetup Mapper application!")

if __name__ == "__main__":
    main()