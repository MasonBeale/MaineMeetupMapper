from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/events")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)