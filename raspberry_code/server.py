#--------------------------------

# Imports
from flask import Flask, request, jsonify
from database import (
    init_db,
    log_error,
    get_all_error_logs
)
#--------------------------------

# Init
app = Flask(__name__)
init_db()
#--------------------------------

# Basic homepage
@app.route("/")
def home():
    return "Log server running."
#--------------------------------

# App methods
@app.route("/log", methods=["POST"])
def log_entry():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400
    try:
        add_log(message)
        return jsonify({"status": "log added"})
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to log entry"}), 500

@app.route("/logs", methods=["GET"])
def list_logs():
    try:
        logs = get_all_logs()
        return jsonify(logs)
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to retrieve logs"}), 500
#--------------------------------

# Temporary main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
