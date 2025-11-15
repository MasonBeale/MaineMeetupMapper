#
# startup.py
# creates a MMM database 
# loads all tables and procedures
#
import sys
import os
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
mycursor.execute('CREATE TABLE IF NOT EXISTS tests (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))')
mycursor.execute('CREATE TABLE IF NOT EXISTS user (user_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))')
mycursor.execute('CREATE TABLE IF NOT EXISTS event (event_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))')
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)

def find_sql_files(directory):
    sql_files = []
    root_path = Path(directory)
    for sql_file in root_path.rglob("*.sql"):
        sql_files.append(sql_file)
    return sql_files
table_files = find_sql_files('./tables/')
procedure_files = find_sql_files('./procedures/')
def execute_sql_files(files):
    for file in files:
        with open(file, 'r') as f:
            sql_script = f.read()
            mycursor.execute(sql_script)
execute_sql_files(table_files)
execute_sql_files(procedure_files)
print(procedure_files)
mydb.commit()