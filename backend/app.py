from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from backend_analytics import BackendAnalytics
import MySQLdb.cursors
import os

app = Flask(__name__)
#Session
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True  # True if running over HTTPS

# Config
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")  # update for security
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "mmmdb"

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Allow your Next.js origin
CORS(app, supports_credentials=True, origins=["http://localhost:3001","http://127.0.0.1:3001"])

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
        # Get ALL filter parameters from frontend
        search = request.args.get('search', '')
        city = request.args.get('city', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        sort_by = request.args.get('sort_by', 'date')  # date, name, rating, popular
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Build query
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
        
        # Add city filter - NEW!
        if city and city != 'all':
            query += " AND l.city = %s"
            params.append(city)
        
        # Add date range filters - NEW!
        if start_date:
            query += " AND e.event_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND e.event_date <= %s"
            params.append(end_date)
        
        query += " GROUP BY e.event_id"
        
        # Add sorting - NEW!
        if sort_by == 'name':
            query += " ORDER BY e.event_name ASC"
        elif sort_by == 'rating':
            query += " ORDER BY avg_rating DESC"
        elif sort_by == 'popular':
            query += " ORDER BY rsvp_count DESC"
        else:  # default to date
            query += " ORDER BY e.event_date ASC"
        
        # Add pagination - NEW!
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Get total count for pagination
        count_query = """
            SELECT COUNT(DISTINCT e.event_id) as total
            FROM event e
            LEFT JOIN location l ON e.location_id = l.location_id
            WHERE 1=1
        """
        count_params = []
        
        if search:
            count_query += " AND (e.event_name LIKE %s OR e.description LIKE %s)"
            count_params.extend([search_param, search_param])
        
        if city and city != 'all':
            count_query += " AND l.city = %s"
            count_params.append(city)
        
        if start_date:
            count_query += " AND e.event_date >= %s"
            count_params.append(start_date)
        
        if end_date:
            count_query += " AND e.event_date <= %s"
            count_params.append(end_date)
        
        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()['total']
        
        # Format the results (same as before)
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
                'state': 'ME',
                'organizer': f"{event['organizer_first_name']} {event['organizer_last_name']}" if event['organizer_first_name'] else 'Unknown',
                'organizer_email': event['organizer_email'],
                'rsvp_count': event['rsvp_count'] or 0,
                'avg_rating': round(float(event['avg_rating']), 1) if event['avg_rating'] else 0,
                'review_count': event['review_count'] or 0,
                'price': 0
            }
            formatted_events.append(formatted_event)
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'events': formatted_events,
            'total': total_count,
            'limit': limit,
            'offset': offset
        })
    
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

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """API endpoint to fetch analytics data"""
    time_range = request.args.get('range', default='month')
    
    # Validate time_range
    valid_ranges = ['day', 'week', 'month', 'year']
    if time_range not in valid_ranges:
        time_range = 'month'
    
    # Generate analytics data
    analytics_data = BackendAnalytics.generate_analytics_data(time_range)
    
    return jsonify(analytics_data)

@app.post("/api/register")
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT user_id FROM User WHERE username=%s OR email=%s", (username, email))
    existing = cursor.fetchone()
    if existing:
        return jsonify({"error": "User already exists"}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    cursor.execute(
        "INSERT INTO User (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, pw_hash),
    )
    mysql.connection.commit()
    user_id = cursor.lastrowid
    cursor.close()

    session["user_id"] = user_id
    session["username"] = username

    user_obj = {
        "user_id": user_id,
        "username": username,
        "email": email,
    }

    return jsonify({"user": user_obj}), 201

@app.route("/api/login", methods=["POST"])
def login():
    # 1. Get data from frontend
    print("HIT /api/login")
    data = request.get_json()
    username_or_email = data.get("username")
    password = data.get("password")
    print("LOGIN payload:", username_or_email)

    # 2. Query database for user
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Assuming you are logging in with 'username'
    cursor.execute("SELECT * FROM User WHERE username = %s", (username_or_email,)) 
    user = cursor.fetchone() # user will be the dictionary if found, or None if not
    cursor.close()
    print("LOGIN user row:", user)

    if not user:
        print("LOGIN: no user found")
        return jsonify({"error": "Invalid username or password"}), 401

    # IMPORTANT: inspect the stored hash once
    print("LOGIN stored hash:", user["password_hash"])

    # 3. Check credentials
    if bcrypt.check_password_hash(user["password_hash"], password):
        # SUCCESS! Set session and return JSON.
        session['user_id'] = user['user_id']
        print("LOGIN session user_id set to:", session.get("user_id"))
        return jsonify({
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
            }
        }), 200
    else:
        # FAILURE! Return JSON error.
        print("LOGIN failed")
        return jsonify({"error": "Invalid username or password"}), 401


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@app.route("/api/me", methods=["PUT"])
def update_me():
    print("DEBUG: Received request to /api/me with data:", request.get_json())
    user_id = session.get("user_id")
    print("DEBUG: Session user_id:", user_id)
    if not user_id:
        return jsonify({"user": None}), 200

    data = request.get_json() or {}
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    new_password = data.get("password")
    new_email = data.get("email")  # NEW

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    fields = []
    params = []

    if first_name is not None:
      fields.append("first_name = %s")
      params.append(first_name)

    if last_name is not None:
      fields.append("last_name = %s")
      params.append(last_name)

    if new_email is not None:      # NEW
      fields.append("email = %s")
      params.append(new_email)

    if new_password:
      pw_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
      fields.append("password_hash = %s")
      params.append(pw_hash)

    if not fields:
      cursor.close()
      return jsonify({"error": "No changes provided"}), 400

    params.append(user_id)
    query = f"UPDATE User SET {', '.join(fields)} WHERE user_id = %s"
    print(f"DEBUG: SQL Query: {query}")
    print(f"DEBUG: SQL Params: {tuple(params)}")

    cursor.execute(query, tuple(params))
    mysql.connection.commit()

    cursor.execute(
      "SELECT user_id, username, email, first_name, last_name FROM User WHERE user_id = %s",
      (user_id,),
    )
    user = cursor.fetchone()
    cursor.close()
    return jsonify({"user": user}), 200

@app.route("/api/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None}), 200

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT user_id, username, first_name, last_name, email FROM User WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({"user": None}), 200

    return jsonify({"user": user}), 200

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/api/me", methods=["DELETE"])
def delete_me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({"error": "Failed to delete account"}), 500

    cursor.close()
    session.clear()
    return jsonify({"message": "Account deleted"}), 200


