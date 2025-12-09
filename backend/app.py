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

@app.route("/api/events")
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

@app.route("/api/favorites", methods=["GET"])
def get_favorites():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"events": []}), 200

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT
        e.event_id      AS id,
        e.event_name    AS name,
        e.event_date    AS date,
        e.description   AS description,
        e.location_id   AS location_id
        FROM UserFavoriteEvent ufe
        JOIN Event e ON ufe.event_id = e.event_id
        WHERE ufe.user_id = %s
        ORDER BY ufe.favorited_at DESC
        """,
        (user_id,),
    )
    events = cursor.fetchall()
    cursor.close()
    return jsonify({"events": events}), 200


@app.route("/api/favorites/<int:event_id>", methods=["POST"])
def add_favorite(event_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT IGNORE INTO UserFavoriteEvent (user_id, event_id) VALUES (%s, %s)",
        (user_id, event_id),
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Favorited"}), 200


@app.route("/api/favorites/<int:event_id>", methods=["DELETE"])
def remove_favorite(event_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "DELETE FROM UserFavoriteEvent WHERE user_id = %s AND event_id = %s",
        (user_id, event_id),
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Unfavorited"}), 200
