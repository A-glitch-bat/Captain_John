from flask import Flask, request, render_template_string, jsonify
import threading
import webbrowser
import time
from geopy.geocoders import Nominatim

app = Flask(__name__)

# This will store the location from the browser
location_data = {}

# HTML + JavaScript served directly by Flask
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Geo Helper</title>
  <script>
    async function sendLocation() {
      if (!navigator.geolocation) {
        alert("Geolocation not supported.");
        return;
      }

      navigator.geolocation.getCurrentPosition(async (position) => {
        const coords = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };

        // Send to backend
        await fetch("/receive-location", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(coords)
        });

        // Optionally close the tab
        document.body.innerHTML = "<h2>Location sent. You may now close this tab.</h2>";
      });
    }

    window.onload = sendLocation;
  </script>
</head>
<body>
  <h1>Fetching location...</h1>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/receive-location', methods=['POST'])
def receive_location():
    global location_data
    location_data = request.json
    return jsonify({"status": "ok"})

def start_server():
    app.run(port=5000, debug=False)

def get_city_name(lat, lon):
    geolocator = Nominatim(user_agent="geo_locator_app")
    location = geolocator.reverse((lat, lon), language='en')
    if location and "city" in location.raw["address"]:
        return location.raw["address"]["city"]
    elif location:
        return location.raw["address"].get("town") or location.raw["address"].get("village")
    return "Unknown location"

def get_geostats():
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    webbrowser.open("http://localhost:5000")

    while not location_data:
        time.sleep(0.5)

    lat = location_data["latitude"]
    lon = location_data["longitude"]
    city = get_city_name(lat, lon)
    
    
    return [lat, lon, city]