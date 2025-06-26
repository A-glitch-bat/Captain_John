#--------------------------------

# Imports
from flask import Flask, render_template, request, jsonify
from chatbots import Schizobot
"""rom database import (
    init_db,
    log_error,
    get_all_error_logs
)"""
#--------------------------------

# Init
server = Flask(__name__)
schizobot = Schizobot()
"""init_db()
#--------------------------------
"""

# Different requests
@server.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        message = f"Received: {user_input}"
    return render_template('index.html', message=message)
#--------------------------------

@server.route('/bigbot', methods=['POST'])
def ask_bigbot():
    msg = request.form['message']
    reply = msg # ask an actual AI
    return reply

@server.route('/schizobot', methods=['POST'])
def ask_schizobot():
    msg = request.form['message']
    reply = schizobot.get_reply(msg)
    if reply.startswith(msg):
        reply = reply[len(msg):].strip()
    return reply

#--------------------------------

# Database related methods
"""
@server.route("/log", methods=["POST"])
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

@server.route("/logs", methods=["GET"])
def list_logs():
    try:
        logs = get_all_logs()
        return jsonify(logs)
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to retrieve logs"}), 500
#--------------------------------
"""

