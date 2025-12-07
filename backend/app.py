"""
app.py
----------------------------------
Flask REST API for Maine Meetup Mapper
Location endpoints by Logan
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Babystom2!",  # MySQL password
        database="meetup_mapper"
    )

# ============================================
# LOCATION ENDPOINTS - Logan
# ============================================

# GET all locations (with optional zip filter)
@app.route("/api/locations", methods=["GET"])
def get_locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    zip_code = request.args.get("zip")
    
    if zip_code:
        cursor.execute("SELECT * FROM Location WHERE zip_code = %s", (zip_code,))
    else:
        cursor.execute("SELECT * FROM Location")
    
    locations = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(locations)

# GET single location by ID
@app.route("/api/locations/<int:location_id>", methods=["GET"])
def get_location(location_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Location WHERE location_id = %s", (location_id,))
    location = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if location:
        return jsonify(location)
    else:
        return jsonify({"error": "Location not found"}), 404

# GET locations by city
@app.route("/api/locations/city/<city>", methods=["GET"])
def get_locations_by_city(city):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Location WHERE city = %s", (city,))
    locations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(locations)

# POST new location
@app.route("/api/locations", methods=["POST"])
def create_location():
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO Location (venue_name, address, city, zip_code) VALUES (%s, %s, %s, %s)",
        (data["venue_name"], data["address"], data["city"], data["zip_code"])
    )
    
    conn.commit()
    new_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Location created", "location_id": new_id}), 201

# Health check
@app.route("/api/events")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)