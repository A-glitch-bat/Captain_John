#--------------------------------

# Imports
import requests

#--------------------------------

# Info worker updated every second
class UsageThread():
    
    # IP based latitude and longitude
    def get_coordinates(self):
        try:
            response = requests.get("https://ipinfo.io/json")
            if response.status_code == 200:
                data = response.json()
                if "loc" in data:
                    latitude, longitude = map(float, data["loc"].split(","))
                    return [latitude, longitude]
            return None
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
            return None
    #--------------------------------
    
    # Weather info API call
    def get_weather_from_open_meteo(self, lat, lon):
        """
        weather from Open-Meteo API
        """
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "current_weather" in data:
                    weather = {
                        "temperature": data["current_weather"]["temperature"],
                        "wind_speed": "%.2f" % (data["current_weather"]["windspeed"]/3.6),
                        "description": "Current weather data"
                    }
                    return weather
            return {"error": f"Could not retrieve weather information. Error code: {response.status_code}"}
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return {"error": "An unexpected error occurred."}
    #--------------------------------