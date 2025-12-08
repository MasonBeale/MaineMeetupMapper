'''
startup.py
Initializes the database by creating necessary tables and stored procedures.
Requires command line arguments: host, user, password, database_name
@author Mason Beale
'''
import sys
from pathlib import Path
import mysql.connector

mydb = mysql.connector.connect(
    host=sys.argv[1],
    user=sys.argv[2],
    password=sys.argv[3]
)
mycursor = mydb.cursor()

mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {sys.argv[4]}")
mydb = mysql.connector.connect(
    host=sys.argv[1],
    user=sys.argv[2],
    password=sys.argv[3],
    database=sys.argv[4]
)
mycursor = mydb.cursor()

def find_sql_files(directory):
    sql_files = []
    root_path = Path(directory)
    for sql_file in root_path.rglob("*.sql"):
        sql_files.append(sql_file)
    return sql_files
procedure_files = find_sql_files('./procedures_/')

def execute_sql_files(files):
    for file in files:
        with open(file, 'r') as f:
            sql_script = f.read()
            mycursor.execute(sql_script)
 

execute_sql_files([Path('./tables_/location_Table.sql'), Path('./tables_/User_Table.sql'), Path('./tables_/event_table.sql'), Path('./tables_/Category_Table.sql'), Path('./tables_/review_table.sql'), Path('./tables_/RSVP_table.sql')])
execute_sql_files(procedure_files)
mydb.commit()