#--------------------------------

# Imports
import psutil
import shutil
import requests
import subprocess
import torch
import GPUtil

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QTextEdit, QFrame, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QBrush, QPainterPath, QPainter

from elements.glitchwidget import GlitchWidget
from elements.ratio_widgets import PercentageCircleWidget, PercentageBarWidget
import config
#--------------------------------

print("CUDA Available:", torch.cuda.is_available())
print("Using Device:", torch.device("cuda" if torch.cuda.is_available() else "cpu"))

def get_gpu_stats():
    """
    sniffs out the gpus
    """
    # naturally by running shell through python
    cmd = "Get-CimInstance Win32_VideoController | Select-Object Name, Availability"
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=False)

    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(gpu)

    return result

def get_coordinates():
    """
    IP based latitude and longitude
    """
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

def get_weather_from_open_meteo(lat, lon):
    """
    weather data from Open-Meteo API
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

# Classes for separate parts of an L-shaped panel component
#--------------------------------
class TopInfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("INFO_1")
        
        # outer frame
        outer_layout = QVBoxLayout(self)
        outer_layout.setSpacing(0)
        outline_frame = QFrame(self)
        outer_layout.addWidget(outline_frame)

        # content frame
        content_layout = QVBoxLayout(outline_frame)
        self.content_frame = QFrame(outline_frame)
        content_layout.addWidget(self.content_frame)
        title_bar = QHBoxLayout()
        self.content_frame.setLayout(QVBoxLayout())
        self.content_frame.layout().addLayout(title_bar)

        title_label = QLabel("INFO")
        title_label.setStyleSheet("color: hotpink; font: bold 10pt OCR A Extended;")
        title_bar.addWidget(title_label)

        # title bar
        title_bar.addStretch()
        title_label.mousePressEvent = self.start_move
        title_label.mouseMoveEvent = self.on_motion
        #--------------------------------
        self.central_widget = QWidget()

        # CPU, GPU, RAM, disk usage displays
        self.CPU_widget = PercentageCircleWidget(10, "CPU")
        self.RAM_widget = PercentageCircleWidget(50, "RAM")
        total, used, _ = shutil.disk_usage("C:/")
        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        self.space_widget = PercentageBarWidget(total_gb, used_gb, "GB")

        self.content_frame.layout().addWidget(self.space_widget)
        self.content_frame.layout().addWidget(self.CPU_widget)
        self.content_frame.layout().addWidget(self.RAM_widget)

        # Timer to update displays
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)

    # Functions
    #--------------------------------
    def update_usage(self):
        """
        constantly updated CPU and RAM usage displays
        """
        cpu_percent = psutil.cpu_percent(interval=0)

        if self.CPU_widget:
            # remove the previous and add the updated widget
            old_widget = self.content_frame.layout().takeAt(self.content_frame.layout().indexOf(self.CPU_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            self.CPU_widget = PercentageCircleWidget(cpu_percent, "CPU")
            self.content_frame.layout().addWidget(self.CPU_widget)

        ram_percent = psutil.virtual_memory().percent

        if self.RAM_widget:
            # remove the previous and add the updated widget
            old_widget = self.content_frame.layout().takeAt(self.content_frame.layout().indexOf(self.RAM_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            self.RAM_widget = PercentageCircleWidget(ram_percent, "RAM")
            self.content_frame.layout().addWidget(self.RAM_widget)
    #--------------------------------
    def start_move(self, event):
        """
        draggable window logic when moved
        """
        self.click_position = event.globalPos()
    # same purpose ^
    def on_motion(self, event):
        """
        draggable window logic on motion
        """
        delta = event.globalPos() - self.click_position
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.click_position = event.globalPos()
    #--------------------------------
    def paintEvent(self, event):
        """
        paint event for holographic visuals
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # custom outline of the top panel
        path = QPainterPath()
        rect = self.rect()
        radius = 30
        path.moveTo(rect.x() + radius, rect.y()) # start at top-left corner
        path.lineTo(rect.right() - radius, rect.y()) # top edge
        path.lineTo(rect.right(), rect.y() + radius) # top-right corner
        path.lineTo(rect.right(), rect.bottom()) # right edge
        path.lineTo(rect.x() + radius, rect.bottom()) # bottom edge
        path.lineTo(rect.x(), rect.bottom() - radius) # bottom-left corner 
        path.lineTo(rect.x(), rect.y() + radius) # left edge
        path.lineTo(rect.x() + radius, rect.y()) # top-left corner 

        # translucent background
        painter.setBrush(QBrush(QColor(255, 105, 180, 50)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(path)
        
        painter.end()
    #--------------------------------
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.close()
#--------------------------------

class BottomInfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("INFO_2")
        self.got_coords = get_coordinates()
        #--------------------------------
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Text field
        self.text_field = QTextEdit(self)
        self.text_field.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0);
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: none;
            }
        """)
        self.text_field.setReadOnly(True)
        self.text_field.setAttribute(Qt.WA_TranslucentBackground, True)

        # Stack glitch over text
        glitch_overlay = GlitchWidget(self)
        stacked_layout = QStackedLayout()
        stacked_layout.addWidget(self.text_field)
        stacked_layout.addWidget(glitch_overlay)
        stacked_layout.setStackingMode(QStackedLayout.StackAll)

        glitch_container = QWidget()
        glitch_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        glitch_container.setMinimumHeight(100)
        glitch_container.setMinimumWidth(100)

        glitch_container.setLayout(stacked_layout)
        def resize_glitch():
            glitch_overlay.setGeometry(self.text_field.geometry())
        glitch_container.resizeEvent = lambda event: resize_glitch()
        
        if self.got_coords is not None:
            weather_info = get_weather_from_open_meteo(self.got_coords[0], self.got_coords[1])
            if "error" in weather_info:
                print(weather_info["error"])
            else:
                self.text_field.setText(f"Temperature: {weather_info['temperature']}°C \nWind Speed: {weather_info['wind_speed']} m/s")
        else:
            print("Could not determine your location.")
        main_layout.addWidget(glitch_container)
        #--------------------------------

        # Timer to update displays
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(10000)
        #--------------------------------

    # Functions
    #--------------------------------
    def paintEvent(self, event):
        """
        paint event for holographic visuals
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # custom outline of the top panel
        path = QPainterPath()
        rect = self.rect()
        radius = 30
        path.moveTo(rect.x(), rect.y()) # start at top-left corner
        path.lineTo(rect.right(), rect.y()) # top edge
        path.lineTo(rect.right(), rect.bottom() - radius) # right edge
        path.lineTo(rect.right() - radius, rect.bottom()) # bottom-right corner 
        path.lineTo(rect.x() + radius, rect.bottom()) # bottom edge
        path.lineTo(rect.x(), rect.bottom() - radius) # bottom-left corner 
        path.lineTo(rect.x(), rect.y()) # left edge

        # translucent background
        painter.setBrush(QBrush(QColor(255, 105, 180, 50)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(path)
        
        painter.end()
    #--------------------------------
    def update_weather(self):
        """
        weather update every 10 seconds
        """
        if self.got_coords is not None:
            weather_info = get_weather_from_open_meteo(self.got_coords[0], self.got_coords[1])
            if "error" in weather_info:
                print(weather_info["error"])
            else:
                self.text_field.setText(f"Temperature: {weather_info['temperature']}°C \nWind Speed: {weather_info['wind_speed']} m/s")
        else:
            print("Could not determine your location.")
    #--------------------------------
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.close()
#--------------------------------

# Main window class and file main
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setGeometry(int(config.scale*565) + int((config.scale-0.45)*200), # W pos,
                         int((config.scale-0.40)*135), # H pos,
                         int(config.scale*450), int(config.scale*800))  # W size, H size
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.75)

        GPUstats = get_gpu_stats()
        print(GPUstats)

    def init_ui(self):
        """
        Setup UI with top and bottom panels, and overlay EXIT button.
        """
        # create panels and layout
        self.top_panel = TopInfoPanel()
        self.bottom_panel = BottomInfoPanel()
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # add panels with a spacer on the bottom left
        main_layout.addWidget(self.top_panel)
        bottom_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(
            10, 5, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        bottom_layout.addItem(horizontal_spacer)
        bottom_layout.setStretch(0, 1)
        bottom_layout.addWidget(self.bottom_panel)
        bottom_layout.setStretch(1, 2)
        main_layout.addLayout(bottom_layout)

        # close button without own space
        self.exit_button = QPushButton("EXIT", self)
        self.exit_button.setStyleSheet("""
            QPushButton {
                color: hotpink;
                font: bold 10pt OCR A Extended;
                padding: 5px;
                border: 2px solid hotpink;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        self.exit_button.setFixedSize(70, 30)
        self.exit_button.clicked.connect(self.close)
        self.reposition_exit_button()
#--------------------------------
    def resizeEvent(self, event):
        """
        reposition close button on resize
        """
        self.reposition_exit_button()
        super().resizeEvent(event)
#--------------------------------
    def reposition_exit_button(self):
        """
        position close button at the top-right corner
        """
        if self.top_panel:
            top_panel_geometry = self.top_panel.geometry()
            self.exit_button.setGeometry(
                QRect(
                    top_panel_geometry.x() + top_panel_geometry.width() - self.exit_button.width() - 25,
                    top_panel_geometry.y() + 25,
                    self.exit_button.width(),
                    self.exit_button.height(),
                )
            )
#--------------------------------
    def closeEvent(self, _):
        """
        shut down both timers and close app
        """
        self.top_panel.stop_timer()
        self.bottom_panel.stop_timer()
        self.close()
#--------------------------------

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
