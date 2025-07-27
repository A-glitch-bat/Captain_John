#--------------------------------

# Imports
import os
import requests
from PyQt5.QtCore import QThread, pyqtSignal
import config
#--------------------------------

# Info worker updated every second
class RequestsThread(QThread):
    response = pyqtSignal(dict)
    #--------------------------------

    def __init__(self, msg, bot, timeout=5):
        super().__init__()
        self.arg = msg
        self.bot = bot
        self.timeout = timeout

    def run(self):
        """
        send msg to specified bot
        """
        try:
            result = requests.post(url = os.path.join(config.URL, self.bot), 
                                   data=self.arg).text
            self.response.emit({
                "success": True,
                "data": result
            })

        except requests.exceptions.ConnectTimeout:
            self.response.emit({
                "success": False,
                "error": "Connection timed out."
            })
        except requests.exceptions.RequestException as e:
            self.response.emit({
                "success": False,
                "error": f"Request failed: {str(e)}"
            })
        except Exception as e:
            self.response.emit({
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            })
#--------------------------------
