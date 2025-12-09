from pathlib import Path
import configparser
import MySQLdb


class BackendAnalytics:
    
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
            'database': database_name
        }

    @staticmethod
    def get_analytics():
        try:
            config = BackendAnalytics.load_config()
            connection = MySQLdb.connect(
                host=config['host'],
                user=config['user'],
                passwd=config['password'],
                db=config['database']
            )
            cursor = connection.cursor()
            
            # Get total number of users
            cursor.execute("SELECT COUNT(*) as total_users FROM User")
            total_users = cursor.fetchone()[0]
            
            # Get total number of events
            cursor.execute("SELECT COUNT(*) as total_events FROM Event")
            total_events = cursor.fetchone()[0]
            
            # Get total number of locations
            cursor.execute("SELECT COUNT(*) as total_locations FROM Location")
            total_locations = cursor.fetchone()[0]
            
            cursor.close()
            connection.close()
            
            return {
                'totalUsers': total_users,
                'totalEvents': total_events,
                'totalLocations': total_locations
            }
        except Exception as e:
            print(f"Error fetching analytics: {e}")
            return {
                'totalUsers': 0,
                'totalEvents': 0,
                'totalLocations': 0,
                'error': str(e)
            }