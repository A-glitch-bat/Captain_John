#--------------------------------

# Imports
import sys
import subprocess
import os
import webbrowser
import requests

from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer

from panel import MainWindow
from texthead import Chatbot
from speechhead import Speechbot
from main_init import Initializer
from elements.digitrain import DigitalRainPanel
from elements.transparent_img import TransparentImageWidget
import config
#--------------------------------

# Main class
class CustomWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        """
        define all the important jazz
        """
        self.txt_file = config.txt_file
        self.init_class = Initializer()
        self.r_path = os.path.join(config.base_folder, "rust_console/target/release/rust_console.exe")
        B1 = os.path.join(config.destination, "Button1.png")
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        self.V_check = os.path.join(config.destination, "icons/confirm.png")
        self.V_cancel = os.path.join(config.destination, "icons/cancel.png")
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Main interface")
        self.setWindowFlags(Qt.FramelessWindowHint)  # remove window border
        self.setAttribute(Qt.WA_TranslucentBackground)  # transparent background
        Ph = int((config.scale-0.45)*200); Pw = int((config.scale-0.40)*150) # window position
        Wh = int(config.scale*550); Ww = int(config.scale*400) # window size
        self.setGeometry(Ph, Pw, Wh, Ww)
        #--------------------------------

        # Load and set the background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "H_background1.png")
        pixmap = QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        
        # Create custom close button
        self.close_button = QtWidgets.QPushButton("EXIT", self)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
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
        self.close_button.clicked.connect(self.close)
        
        # Create the central widget and horizontal layout for buttons and list
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(int(config.scale*45), int(config.scale*55),
                                       int(config.scale*50), int(config.scale*45)) # L, Up, R, Down
        central_widget.setLayout(main_layout)

        # Create a vertical layout for buttons on the left
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QVBoxLayout()
        button_container.setLayout(button_layout)
        button_container.setMinimumWidth(int(config.scale * 150))
        main_layout.addWidget(button_container, alignment=Qt.AlignLeft)

        #--------------------------------
        # VS Code Button
        open_vscode_button = QtWidgets.QPushButton("CODE")
        open_vscode_button.setMinimumSize(128, 64)
        open_vscode_button.setMaximumSize(128, 64)
        open_vscode_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        open_vscode_button.clicked.connect(self.open_vscode)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        open_vscode_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(open_vscode_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # Info Butoon
        self.init_button = QtWidgets.QPushButton("INIT", self)
        self.init_button.setMinimumSize(128, 64)
        self.init_button.setMaximumSize(128, 64)
        self.init_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        self.init_button.clicked.connect(self.set_init)
        
        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        self.init_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(self.init_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # SSH connection to Raspberry PI
        ssh_button = QtWidgets.QPushButton("RPI", self)
        ssh_button.setMinimumSize(128, 64)
        ssh_button.setMaximumSize(128, 64)
        ssh_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        ssh_button.clicked.connect(self.ssh_to_rpi)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        ssh_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(ssh_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # Testing button
        test_button = QtWidgets.QPushButton("TEST", self)
        test_button.setMinimumSize(128, 64)
        test_button.setMaximumSize(128, 64)
        test_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        test_button.clicked.connect(self.open_rwindow)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        test_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(test_button, alignment=Qt.AlignCenter)
        #--------------------------------

        # Temperature stats
        self.temp_stats = TransparentImageWidget(button_layout.sizeHint(), os.path.join(config.destination, "nightsky.png"))
        button_layout.addWidget(self.temp_stats)
        button_layout.setAlignment(Qt.AlignHCenter)
        button_layout.addStretch()
        #--------------------------------

        # Start the panels
        self.start_chats()
        self.open_info_panel()
        #--------------------------------

        # Create a vertical layout for the list on the right
        list_layout = QtWidgets.QVBoxLayout()
        input_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(list_layout)
        list_layout.addLayout(input_layout)

        # Display TO-DO list
        self.list_display = QtWidgets.QListWidget(self)
        self.list_display.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 125);
                color: hotpink;
                font-family: 'OCR A Extended';
                font-size: 14px;
                border: 2px solid hotpink;
                border-radius: 14px;
                padding: 6px;
            }
        """)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(50)
        effect.setColor(QColor(255, 0, 255, 75))
        effect.setOffset(0, 0)
        self.list_display.setGraphicsEffect(effect)

        self.list_display.setMinimumSize(int(config.scale*128), int(config.scale*128))
        self.list_display.setMaximumSize(int(config.scale*256), int(config.scale*256))
        list_layout.addWidget(self.list_display)

        # Input
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("add to list...")
        self.input_field.returnPressed.connect(self.write_input)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 125);
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
                border-radius: 7px;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.setIcon(QIcon.fromTheme(self.V_check))
        self.submit_button.setFixedSize(32, 32)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid hotpink;
                border-radius: 7px;
            }
        """)
        self.submit_button.clicked.connect(self.write_input)        
        input_layout.addWidget(self.submit_button)
        #--------------------------------

        # Background digital rain
        rainColour = [0, 255, 255] #rainColour = [255, 105, 180] # cyan//hotpink
        self.background_text = DigitalRainPanel([Ph, Pw, Wh, Ww], rainColour, central_widget)
        self.background_text.lower() # Widget to background
        #--------------------------------

        # Weather updates
        self.coords = None
        self.suntime = None
        self.today = datetime.now().date()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(60000)

        # Ensure the app works as intended
        self.read_list()
        self.adjust_close_button_position()
        self.close_button.raise_()
        self.coords = self.init_class.get_geostats()
        self.suntime = self.init_class.daytime_calculator(self.coords[0], self.coords[1], self.today)
        self.update_weather()
    #--------------------------------

    # Functions
    #--------------------------------
    def adjust_close_button_position(self):
        """
        re-position close button to top-right corner
        before raising (based on window size)
        """
        self.close_button.setGeometry(self.width() - int(config.scale*60), int(config.scale*30),
                                      int(config.scale*50), int(config.scale*30)) # L, H, R, W
    #--------------------------------
    def open_vscode(self):
        folder_path = "C:/John"
        subprocess.Popen(["code", folder_path], shell=True)
    #--------------------------------
    def set_init(self):
        self.init_class.init_button()
    #--------------------------------
    def open_info_panel(self):
        """
        open InfoPanel on button click
        """
        self.info_panel = MainWindow() # prevent garbage-collection
        self.info_panel.show()
    #--------------------------------
    def start_chats(self):
        """
        open chat AIs on button click
        """
        self.aihead = Chatbot()
        self.aihead.show()

        self.listdisplay = Speechbot()
        self.listdisplay.show()
    #--------------------------------
    def ssh_to_rpi(self):
        subprocess.Popen(["start", "cmd", "/k", "ssh raspberrypi"], shell=True)
    #--------------------------------
    def write_input(self):
        """
        write text to file
        """
        input_text = self.input_field.text()
        if input_text: # input exists
            self.append_text(self.txt_file, input_text)
            self.input_field.clear() #clear
            self.read_list()
    # sub-function ^
    def append_text(self, file_path, text):
        """
        open file, append text, close file
        """
        with open(file_path, "a+") as file:
            file.seek(0, 2) # pointer to the end of the file
            if file.tell() > 0:
                file.seek(file.tell() - 1) # find last character
                last_char = file.read(1)
                if last_char != "\n": # confirm new line
                    file.write("\n")
            file.write(text)
    # sub-function ^
    def delete_item(self, item, item_text, checkbox):
        """
        delete the line from the text file and remove 
        the list item if the checkbox is checked
        """
        #print(checkbox)
        if checkbox == 1:
            # delete line if checkbox is ticked
            with open(self.txt_file, "r") as file:
                lines = file.readlines()
            with open(self.txt_file, "w") as file:
                for line in lines:
                    if line.strip() != item_text:
                        file.write(line)

            # also remove from the list widget
            row = self.list_display.row(item)
            self.list_display.takeItem(row)
    #--------------------------------
    def read_list(self):
        """
        text file display
        """
        try:
            with open(self.txt_file, "r") as file:
                lines = file.readlines()
            self.list_display.clear()
            for line in lines:
                line = line.strip()
                self.add_list_item(line)
        except FileNotFoundError:
            self.list_display.clear()
            self.list_display.addItem("Error: 'list.txt' not found.")
    # sub-function ^
    def add_list_item(self, text):
        """
        add a line of text to the list widget
        """
        row_widget = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setContentsMargins(2, 2, 2, 2)
        row_layout.setSpacing(5)

        # create checkbox, text label and delete button
        checkbox = QtWidgets.QCheckBox()
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: hotpink;
            }
        """)
        checkbox.stateChanged.connect(lambda checked, text=text: self.checkbox_toggle_visual(checked, text))
        text_label = QtWidgets.QLabel(text)
        text_label.setStyleSheet("color: hotpink; font-size: 14px; font-family: OCR A Extended;")

        delete_button = QtWidgets.QPushButton()
        delete_button.setIcon(QIcon(self.V_cancel))
        delete_button.setIconSize(QSize(24, 24))
        delete_button.setFixedSize(30, 30)
        delete_button.setStyleSheet("border: none;")

        # checkbox -> text -> delete button
        row_layout.addWidget(checkbox)
        row_layout.addWidget(text_label)
        row_layout.addWidget(delete_button)

        row_layout.setAlignment(Qt.AlignLeft)
        row_widget.setLayout(row_layout)
        list_item = QtWidgets.QListWidgetItem(self.list_display)
        list_item.setSizeHint(row_widget.sizeHint())
        self.list_display.setItemWidget(list_item, row_widget)

        # delete button click connection
        delete_button.clicked.connect(lambda: self.delete_item(list_item, text, checkbox.isChecked()))
    #--------------------------------
    def checkbox_toggle_visual(self, state, text):
        """
        checkbox toggling visual effect
        """
        for i in range(self.list_display.count()):
            widget_item = self.list_display.item(i)
            row_item = self.list_display.itemWidget(widget_item)
            item_label = row_item.findChild(QtWidgets.QLabel)
            if item_label.text() == text:
                if state == 2:
                    font = item_label.font()
                    font.setStrikeOut(True)
                    item_label.setFont(font)
                    item_label.setStyleSheet("color: rgba(255, 105, 180, 100);")
                elif state == 0:
                    font = item_label.font()
                    font.setStrikeOut(False)
                    item_label.setFont(font)
                    item_label.setStyleSheet("color: hotpink;")
    #--------------------------------
    def open_rwindow(self):
        """
        rust console call
        """
        rust_project_dir = os.path.join(config.base_folder, "rust_console")
        subprocess.Popen([self.r_path], cwd=rust_project_dir)
        webbrowser.open("http:localhost:3000")
    #--------------------------------
    def update_weather(self):
        """
        called periodically to update weather status
        """
        if self.coords:
            # compare sundown and sunrise times and update when needed
            self.today = datetime.now().date()
            if self.today > self.suntime[0]:
                self.suntime = self.init_class.daytime_calculator(self.coords[0], self.coords[1], self.today)
            if self.suntime[1] < datetime.now() and datetime.now() < self.suntime[2]:
                text = "Sunset\nat "+self.suntime[2].strftime("%H:%M")
                if self.temp_stats.caption_label.text() != text:
                    self.temp_stats.swap_daytime_png("day", text)
            else:
                text = "Sunrise\nat "+self.suntime[1].strftime("%H:%M")
                if self.temp_stats.caption_label.text() != text:
                    self.temp_stats.swap_daytime_png("night", text)

            # get and display new nurrent weather
            new_weath = self.get_weather_from_open_meteo(self.coords[0], self.coords[1])

            self.temp_stats.text_field.setText(
                f"{new_weath['temperature']}°C\n"
                f"{self.wind_description(new_weath['wind_speed'])}\n"
                f"{self.coords[2]}"
            )
            self.temp_stats.text_field.setAlignment(Qt.AlignmentFlag.AlignBottom)
    # sub-function ^
    def wind_description(self, speed_mps):
        """
        convert wind speed to description
        """
        thresholds = [0.5, 1.6, 5.5, 10.8]
        labels = ["calm", "light air", "breezy", "windy", "stormy"]
        print(speed_mps)

        for i, threshold in enumerate(thresholds):
            if speed_mps < threshold:
                return labels[i]
        return labels[-1]
    #--------------------------------
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
                        "wind_speed": data["current_weather"]["windspeed"]/3.6,
                        "description": "Current weather data"
                    }
                    return weather
            return {"error": f"Could not retrieve weather information. Error code: {response.status_code}"}
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return {"error": "An unexpected error occurred."}
    #--------------------------------

#--------------------------------
# Wake John up
app = QtWidgets.QApplication(sys.argv)
window = CustomWindow()
window.show()
sys.exit(app.exec_())
#--------------------------------
