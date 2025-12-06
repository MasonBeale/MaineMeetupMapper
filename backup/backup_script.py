import subprocess
import datetime
from pathlib import Path

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'mmmdb3'
}

MYSQLDUMP_PATH = r'C:\Program Files\MySQL\MySQL Server 9.5\bin\mysqldump.exe'  # UPDATE THIS
BACKUP_DIR = Path('./backup/backups')
BACKUP_DIR.mkdir(exist_ok=True)

def create_backup():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = BACKUP_DIR / f"mmmdb3_backup_{timestamp}.sql"
    
    cmd = [
        MYSQLDUMP_PATH,
        f"--host={DB_CONFIG['host']}",
        f"--user={DB_CONFIG['user']}",
        f"--password={DB_CONFIG['password']}",
        '--single-transaction',
        '--routines',
        '--triggers',
        '--set-gtid-purged=OFF',
        DB_CONFIG['database']
    ]
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        subprocess.run(cmd, stdout=f, check=True)
    
    size_kb = backup_file.stat().st_size / 1024
    print(f"Backup created: {backup_file.name} ({size_kb:.2f} KB)")
    return backup_file

def list_backups():
    backups = sorted(BACKUP_DIR.glob('*.sql'), reverse=True)
    
    for backup in backups:
        mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"  {backup.name} - {mtime}")

if __name__ == "__main__":
    print(f"Backing up database: {DB_CONFIG['database']}")
    create_backup()
    print("\nAll backups:")
    list_backups()