from flask import Flask, jsonify, request
from flask_cors import CORS
from backend_analytics import BackendAnalytics

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)