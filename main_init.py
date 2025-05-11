#--------------------------------

# Imports
from flask import Flask, request, render_template_string, jsonify
from geopy.geocoders import Nominatim
import os
import threading
import webbrowser
import time
import pygetwindow as gw
import win32gui
import win32con
#--------------------------------

# Init task class
class Initializer():
    def __init__(self):
        """
        define all the important jazz
        """
        self.app = Flask(__name__)
        self.location_data = {}
        self.html_path = os.path.join(os.path.dirname(__file__), "tasks/geohelper.html")

        # Route definitions
        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/receive-location", view_func=self.receive_location, methods=["POST"])
        #--------------------------------

    def init_button(self):
        return "todo"
    
    def index(self):
        with open(self.html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return render_template_string(html_content)

    def receive_location(self):
        self.location_data = request.json
        return jsonify({"status": "ok"})

    def start_server(self):
        self.app.run(port=5000, debug=False)

    def get_city_name(self, lat, lon):
        geolocator = Nominatim(user_agent="geo_locator_app")
        location = geolocator.reverse((lat, lon), language='en')
        if location and "city" in location.raw["address"]:
            return location.raw["address"]["city"]
        elif location:
            return location.raw["address"].get("town") or location.raw["address"].get("village")
        return "Unknown location"

    def get_geostats(self):
        threading.Thread(target=self.start_server, daemon=True).start()
        time.sleep(1)
        webbrowser.open("http://localhost:5000")

        while not self.location_data:
            time.sleep(0.5)

        lat = self.location_data["latitude"]
        lon = self.location_data["longitude"]
        city = self.get_city_name(lat, lon)

        # minimize Chrome
        time.sleep(2)
        for window in gw.getWindowsWithTitle('Chrome'):
            if window.visible and not window.isMinimized:
                hwnd = window._hWnd
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                break

        return [lat, lon, city]