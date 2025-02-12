#--------------------------------

# Imports
import psutil
import subprocess
import json
import requests
import time
import GPUtil
from PyQt5.QtCore import QThread, pyqtSignal

#--------------------------------

class UsageThread(QThread):
    data_updated = pyqtSignal(dict)  # Signal to send back data
    #--------------------------------

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

    # Get GPU stats
    def get_gpu_stats(self):
        """
        sniffs out the gpus
        """
        # naturally by running shell through python
        cmd = "Get-WmiObject Win32_VideoController | Select-Object Name, Availability | ConvertTo-Json"
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            ["powershell", "-Command", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo
        )
        
        stdout, stderr = process.communicate()
        
        if stderr:
            print("Error:", stderr)
            return None, None
        
        gpu_info = json.loads(stdout)
        gpus = GPUtil.getGPUs()
        
        return gpu_info, gpus
    #--------------------------------

    def run(self):
        self.got_coords = self.get_coordinates()
        while True:
            GPUinfo, GPUstats = self.get_gpu_stats()
            if self.got_coords is not None:
                weather_info = self.get_weather_from_open_meteo(self.got_coords[0], self.got_coords[1])
                if "error" in weather_info:
                    print(weather_info["error"])
            else:
                print("Could not determine your location.")
            data = {
                "cpu": psutil.cpu_percent(interval=0),
                "gpu": GPUinfo["Name"],
                "ram": psutil.virtual_memory().percent,
                "temp": str(GPUstats[0].temperature)+"°C",
                "weaTemp": weather_info['temperature'],
                "weaWind": weather_info['wind_speed']
            }
            self.data_updated.emit(data)  # Send data back to UI
            time.sleep(1)  # Wait for 1 second
#--------------------------------