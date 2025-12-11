import mysql.connector
def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    base_dir = Path(__file__).parent
    possible_paths = [
        Path(config_file),
        base_dir / config_file,
        base_dir.parent / config_file,
        base_dir.parent / 'Database_Startup' / config_file,
        Path.cwd() / config_file,
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
config = load_config()

DB_CONFIG = {
    'host': config["host"],
    'user': config["user"],
    'password': config["password"],
    'database': config["database"]
}

def detect_columns():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        tables = ['event', 'location', 'category', 'user', 'review', 'rsvp']
        
        for table in tables:
            print(f"\n{'='*50}")
            print(f"Table: {table}")
            print('='*50)
            
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            
            for col in columns:
                field_name = col[0]
                field_type = col[1]
                print(f"  {field_name:20} | {field_type}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    detect_columns()
