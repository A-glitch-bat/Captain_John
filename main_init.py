#--------------------------------

# Imports
import os
import time
import math
import threading
import webbrowser

from flask import Flask, request, render_template_string, jsonify
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
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

    def daytime_calculator(self, latitude, longitude, date):
        # solar angle on given date, constrained by summer and winter solstice (+23.44° and −23.44°)
        day = date.timetuple().tm_yday
        decl = math.radians(-23.44 * math.cos(math.radians((360 / 365) * (day + 10))))

        # hour angle (in radians)
        lat_rad = math.radians(latitude)
        zenith = math.radians(90.833)
        cosH = (math.cos(zenith) - math.sin(lat_rad) * math.sin(decl)) / (math.cos(lat_rad) * math.cos(decl))
        
        # check for edge cases (polar night or day)
        if abs(cosH) > 1:
            return None, None

        # time difference from midday
        H = math.acos(cosH)
        time_diff = math.degrees(H) / 15

        # solar noon according to longitude, adjusted for timezone difference
        timezone_offset = datetime.now().astimezone().utcoffset().total_seconds() / 3600
        solar_noon = 12 - (longitude / 15) + timezone_offset

        # sunrise and sunset according to local solar noon and time difference
        sunrise = solar_noon - time_diff
        sunset = solar_noon + time_diff
        sunrise_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=sunrise)
        sunset_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=sunset)

        return [date, sunrise_time, sunset_time]

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

# Temporary main
if __name__ == "__main__":
    initTest = Initializer()

    # get UTC sunrise/sunset for today's date
    lat = 46.04887; lon = 14.48018
    todays_date = datetime.now().date()
    dayStats = initTest.daytime_calculator(lat, lon, todays_date)

    # check it out
    print(dayStats[0]); print(dayStats[1]); print(dayStats[2])