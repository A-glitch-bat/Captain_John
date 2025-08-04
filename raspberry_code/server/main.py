#--------------------------------

# Imports
import time
import threading
from flask import Flask, render_template, request, jsonify
from raspberry_code.chatbots import Routerbot, Schizobot, summarize
from raspberry_code.server.database import (
    init_db,
    log_error,
    get_all_error_logs,
    log_performance,
    get_performance
)
#--------------------------------

# Init
server = Flask(__name__)
routerbot = Routerbot()
schizobot = Schizobot()
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

# The bots
@server.route('/routerbot', methods=['POST'])
def ask_routerbot():
    msg = request.form['message']
    return routerbot.classify(msg)

@server.route('/mainbot', methods=['POST'])
def ask_mainbot():
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

@server.route('/sumbot', methods=['POST'])
def ask_sumbot():
    msg = request.form['message']
    return summarize(msg)
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
#--------------------------------

# System stats automatic logging
def sys_stats_logger():
    while True:
        try:
            log_performance()
        except Exception as e:
            log_error("SystemStatsError", str(e))
        time.sleep(600)  # log every 10 minutes

threading.Thread(target=sys_stats_logger, daemon=True).start()

@server.route("/getsys", methods=["GET"])
def list_sys_stats():
    try:
        logs = get_performance()
        return jsonify(logs)
    except Exception as e:
        log_error(type(e).__name__, str(e))
        return jsonify({"error": "Failed to retrieve logs"}), 500
#--------------------------------
