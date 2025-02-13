#--------------------------------

# Imports
import psutil
import wmi
import requests
import time
import pythoncom
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetTemperature, NVML_TEMPERATURE_GPU, nvmlShutdown
from PyQt5.QtCore import QThread, pyqtSignal

#--------------------------------

# Optimized GPU handle
class GPUInfo:
    def __init__(self):
        nvmlInit()
        self.handle = nvmlDeviceGetHandleByIndex(0) # index NVIDIA

    def get_temperature(self):
        return nvmlDeviceGetTemperature(self.handle, NVML_TEMPERATURE_GPU)

    def close(self):
        nvmlShutdown() # cleanup
#--------------------------------

# Info worker updated every second
class UsageThread(QThread):
    data_updated = pyqtSignal(dict) # data signal
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

    # GPU stats for integrated and NVIDIA
    def gpu_info(self):
        pythoncom.CoInitialize() # COM init for wmi in separate thread
        try:
            gpu_info = []
            w = wmi.WMI()
            
            for gpu in w.Win32_VideoController():
                gpu_info.append({
                    "Name": gpu.Name,
                    "Availability": gpu.Availability,
                    "DriverVersion": gpu.DriverVersion,
                    "AdapterRAM": gpu.AdapterRAM,
                    "VideoProcessor": gpu.VideoProcessor
                })
            
            return gpu_info
        finally:
            pythoncom.CoUninitialize() # COM cleanup
    # sub-function ^
    def get_gpu_stats(self):
        gpu_info = self.gpu_info()
        
        return gpu_info
    #--------------------------------

    def run(self):
        self.got_coords = self.get_coordinates()
        self.gpu_monitor = GPUInfo()
        while True:
            GPUinfo = self.get_gpu_stats()
            if self.got_coords is not None:
                weather_info = self.get_weather_from_open_meteo(self.got_coords[0], self.got_coords[1])
                if "error" in weather_info:
                    print(weather_info["error"])
            else:
                print("Could not determine your location.")
            data = {
                "cpu": psutil.cpu_percent(interval=0),
                "gpu": GPUinfo[0]["Name"],
                "ram": psutil.virtual_memory().percent,
                "temp": str(self.gpu_monitor.get_temperature())+"°C",
                "weaTemp": weather_info['temperature'],
                "weaWind": weather_info['wind_speed']
            }
            self.data_updated.emit(data) # send data back to UI
            time.sleep(1) # 1 second refresh timer
#--------------------------------