from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration - UPDATE THESE
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # CHANGE THIS
    'database': 'mmmdb3'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route("/api/events", methods=['GET'])
def get_events():
    """Get all events with optional filtering"""
    try:
        # Get query parameters for filtering
        search = request.args.get('search', '')
        category_id = request.args.get('category')
        date_filter = request.args.get('date')
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Build query with JOINs - using correct column names
        query = """
            SELECT 
                e.event_id,
                e.event_name,
                e.description,
                e.event_date,
                e.start_time,
                e.end_time,
                e.max_capacity,
                l.venue_name,
                l.address,
                l.city,
                l.zip_code,
                u.first_name as organizer_first_name,
                u.last_name as organizer_last_name,
                u.email as organizer_email,
                COUNT(DISTINCT r.RSVP_id) as rsvp_count,
                AVG(rev.rating) as avg_rating,
                COUNT(DISTINCT rev.review_id) as review_count
            FROM event e
            LEFT JOIN location l ON e.location_id = l.location_id
            LEFT JOIN user u ON e.organizer_id = u.user_id
            LEFT JOIN rsvp r ON e.event_id = r.event_id AND r.RSVP_status = 'Going'
            LEFT JOIN review rev ON e.event_id = rev.event_id
            WHERE 1=1
        """
        
        params = []
        
        # Add search filter
        if search:
            query += " AND (e.event_name LIKE %s OR e.description LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        # Add date filter
        if date_filter == 'today':
            query += " AND DATE(e.event_date) = CURDATE()"
        elif date_filter == 'weekend':
            query += " AND DAYOFWEEK(e.event_date) IN (1, 7)"
        elif date_filter == 'upcoming':
            query += " AND e.event_date >= CURDATE()"
        
        query += " GROUP BY e.event_id ORDER BY e.event_date ASC"
        
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Format the results
        formatted_events = []
        for event in events:
            formatted_event = {
                'id': event['event_id'],
                'name': event['event_name'],
                'description': event['description'],
                'date': event['event_date'].isoformat() if event['event_date'] else None,
                'time': str(event['start_time']) if event['start_time'] else None,
                'end_time': str(event['end_time']) if event['end_time'] else None,
                'max_capacity': event['max_capacity'],
                'location': event['venue_name'],
                'address': event['address'],
                'city': event['city'],
                'zip_code': event['zip_code'],
                'state': 'ME',  # Assuming Maine since it's MaineMeetupMapper
                'organizer': f"{event['organizer_first_name']} {event['organizer_last_name']}" if event['organizer_first_name'] else 'Unknown',
                'organizer_email': event['organizer_email'],
                'rsvp_count': event['rsvp_count'] or 0,
                'avg_rating': round(float(event['avg_rating']), 1) if event['avg_rating'] else 0,
                'review_count': event['review_count'] or 0,
                'price': 0  # Your database doesn't have price field, defaulting to free
            }
            formatted_events.append(formatted_event)
        
        cursor.close()
        connection.close()
        
        return jsonify(formatted_events)
    
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/events/<int:event_id>", methods=['GET'])
def get_event_detail(event_id):
    """Get detailed information about a specific event"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Get event details with correct column names
        query = """
            SELECT 
                e.*,
                l.venue_name,
                l.address,
                l.city,
                l.zip_code,
                u.first_name as organizer_first_name,
                u.last_name as organizer_last_name,
                u.email as organizer_email,
                u.username as organizer_username
            FROM event e
            LEFT JOIN location l ON e.location_id = l.location_id
            LEFT JOIN user u ON e.organizer_id = u.user_id
            WHERE e.event_id = %s
        """
        
        cursor.execute(query, (event_id,))
        event = cursor.fetchone()
        
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        # Get reviews for this event
        review_query = """
            SELECT 
                r.review_id,
                r.rating,
                r.comments,
                u.first_name,
                u.last_name,
                u.username
            FROM review r
            LEFT JOIN user u ON r.user_id = u.user_id
            WHERE r.event_id = %s
            ORDER BY r.review_id DESC
        """
        cursor.execute(review_query, (event_id,))
        reviews = cursor.fetchall()
        
        # Get RSVP count (only "Going" status)
        rsvp_query = "SELECT COUNT(*) as count FROM rsvp WHERE event_id = %s AND RSVP_status = 'Going'"
        cursor.execute(rsvp_query, (event_id,))
        rsvp_result = cursor.fetchone()
        
        # Format the response
        formatted_event = {
            'id': event['event_id'],
            'name': event['event_name'],
            'description': event['description'],
            'date': event['event_date'].isoformat() if event['event_date'] else None,
            'time': str(event['start_time']) if event['start_time'] else None,
            'end_time': str(event['end_time']) if event['end_time'] else None,
            'max_capacity': event['max_capacity'],
            'price': 0,  # No price field in database
            'location': {
                'name': event['venue_name'],
                'address': event['address'],
                'city': event['city'],
                'state': 'ME',  # Assuming Maine
                'zip_code': event['zip_code']
            },
            'category': None,  # No category link in your event table
            'organizer': {
                'name': f"{event['organizer_first_name']} {event['organizer_last_name']}" if event['organizer_first_name'] else 'Unknown',
                'username': event['organizer_username'],
                'email': event['organizer_email'],
                'phone': None  # No phone field in user table
            },
            'rsvp_count': rsvp_result['count'] if rsvp_result else 0,
            'reviews': [
                {
                    'id': r['review_id'],
                    'rating': r['rating'],
                    'comment': r['comments'],
                    'user_name': f"{r['first_name']} {r['last_name']}" if r['first_name'] else r['username']
                }
                for r in reviews
            ],
            'avg_rating': sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
        }
        
        cursor.close()
        connection.close()
        
        return jsonify(formatted_event)
    
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/categories", methods=['GET'])
def get_categories():
    """Get all event categories"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(categories)
    
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    print(f"Database: {DB_CONFIG['database']}")
    app.run(debug=True, port=5000)