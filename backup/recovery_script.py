import subprocess
import sys
import datetime
from pathlib import Path

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'mmmdb3'
}

MYSQL_PATH = r'C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe'

def list_backups():
    backup_dir = Path('./backup/backups')
    backups = sorted(backup_dir.glob('*.sql'), key=lambda x: x.stat().st_mtime, reverse=True)
    
    for i, backup in enumerate(backups, 1):
        mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{i}. {backup.name} - {mtime}")
    
    return backups

def restore_backup(backup_file):
    confirm = input(f"\nRestore {backup_file.name}? Type YES: ")
    if confirm != 'YES':
        return False
    
    # Drop and recreate database
    drop_cmd = [
        MYSQL_PATH,
        f"--host={DB_CONFIG['host']}",
        f"--user={DB_CONFIG['user']}",
        f"--password={DB_CONFIG['password']}",
        '-e',
        f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}; CREATE DATABASE {DB_CONFIG['database']};"
    ]
    subprocess.run(drop_cmd, check=True)
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    lines = sql_content.split('\n')
    filtered_lines = [line for line in lines if 'GTID_PURGED' not in line]
    filtered_sql = '\n'.join(filtered_lines)
    
    # Restore
    restore_cmd = [
        MYSQL_PATH,
        f"--host={DB_CONFIG['host']}",
        f"--user={DB_CONFIG['user']}",
        f"--password={DB_CONFIG['password']}",
        DB_CONFIG['database']
    ]
    
    result = subprocess.run(restore_cmd, input=filtered_sql, text=True, capture_output=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    print("Database restored")
    return True

if __name__ == "__main__":
    backups = list_backups()
    if not backups:
        print("No backups found")
        sys.exit(1)
    
    choice = input("\nSelect backup number: ")
    selected = backups[int(choice) - 1]
    restore_backup(selected)