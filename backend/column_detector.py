import mysql.connector

# UPDATE YOUR CREDENTIALS
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # CHANGE THIS
    'database': 'mmmdb3'
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
