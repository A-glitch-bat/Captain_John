#--------------------------------

# Imports
import psutil
import wmi
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

    # GPU stats for integrated and NVIDIA
    def gpu_info(self):
        pythoncom.CoInitialize() # COM init for wmi in separate thread
        try:
            gpu_info = []
            w = wmi.WMI()
            
            for gpu in w.Win32_VideoController():
                gpu_info.append({
                    "Name": gpu.Name,
                    "Status": gpu.Status
                })
            
            return gpu_info
        finally:
            pythoncom.CoUninitialize() # COM cleanup
    # sub-function ^
    def get_gpu_stats(self):
        gpu_info = self.gpu_info()
        #print(gpu_info)
        return gpu_info
    #--------------------------------

    def run(self):
        self.gpu_monitor = GPUInfo()
        while True:
            GPUinfo = self.get_gpu_stats()
            data = {
                "cpu": psutil.cpu_percent(interval=0),
                "gpus": GPUinfo,
                "ram": psutil.virtual_memory().percent,
                "temp": str(self.gpu_monitor.get_temperature())+"°C"
            }
            self.data_updated.emit(data) # send data back to UI
            time.sleep(1) # 1 second refresh timer
#--------------------------------