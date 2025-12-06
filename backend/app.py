from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from backend_analytics import BackendAnalytics
import MySQLdb.cursors
import os

app = Flask(__name__)

# Config
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")  # change in prod

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",        
        database="mmdb"  
    )

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Allow your Next.js origin
CORS(app, supports_credentials=True, origins=["http://localhost:3001","http://127.0.0.1:3000"])

@app.route("/api/events")
# Redefine for events endpoint
def health():
    return jsonify({"status": "ok"})

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

    return jsonify({"user_id": user_id, "username": username, "email": email}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Adjust column names/table to match your schema
    cursor.execute(
        "SELECT userid, email, password_hash FROM users WHERE email = %s",
        (email,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["userid"] = user["userid"]
    session["email"] = user["email"]

    return jsonify({
        "message": "Logged in",
        "user": {
            "userid": user["userid"],
            "email": user["email"],
        }
    }), 200

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@app.route("/api/me", methods=["GET", "PUT"])
def me():
    user_id = session.get("user_id")
    if "userid" not in session:
        return jsonify({"user": None}), 200

    return jsonify({
        "user": {
            "userid": session["userid"],
            "email": session["email"],
        }
    }), 200

if __name__ == "__main__":
    app.run(debug=True)