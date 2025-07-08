#--------------------------------

# Imports
from flask import Flask, render_template, request, jsonify
from chatbots import Schizobot
from server.database import (
    init_db,
    log_error,
    get_all_error_logs,
    log_performance,
    get_performance
)
#--------------------------------

# Init
server = Flask(__name__)
#schizobot = Schizobot() RETURN THIS TO RUNNING CODE BEFORE COMMITTING
init_db()
#--------------------------------

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
"""
@server.route('/schizobot', methods=['POST'])
def ask_schizobot():
    msg = request.form['message']
    reply = schizobot.get_reply(msg)
    if reply.startswith(msg):
        reply = reply[len(msg):].strip()
    return reply
"""
#--------------------------------

# Database related methods
@server.route("/logerr", methods=["POST"])
def log_err():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400
    try:
        log_error(message)
        return jsonify({"status": "log added"})
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to log entry"}), 500

@server.route("/geterr", methods=["GET"])
def list_err_logs():
    try:
        logs = get_all_error_logs()
        return jsonify(logs)
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to retrieve logs"}), 500

@server.route("/logsys", methods=["POST"])
def log_sys_stats():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400
    try:
        log_performance(message)
        return jsonify({"status": "log added"})
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to log entry"}), 500

@server.route("/getsys", methods=["GET"])
def list_sys_stats():
    try:
        logs = get_performance()
        return jsonify(logs)
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to retrieve logs"}), 500
#--------------------------------
