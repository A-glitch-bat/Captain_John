#--------------------------------

# Imports
import os
import sys
import subprocess
import webbrowser
import requests

from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QRadioButton, QHBoxLayout, QVBoxLayout, QButtonGroup, QWidget)
from PyQt5.QtGui import QColor, QPixmap, QIcon, QImage, QPainter
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint

from panel import MainWindow
from texthead import Chatbot
from speechhead import Speechbot
from main_init import Initializer
from elements.digitrain import DigitalRainPanel
from elements.transparent_img import TransparentImageWidget

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
import config
#--------------------------------

# Main class
class CustomWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.f_path = os.path.dirname(os.path.abspath(__file__))
        print(self.f_path)
        """
        define all the important jazz
        """
        self.init_class = Initializer()
        self.txt_file = os.path.join(self.f_path, "list.txt")
        self._drag_pos = None
        B1 = os.path.join(self.f_path, "visuals/Button1.png").replace("\\", "/")
        B2 = os.path.join(self.f_path, "visuals/Button2.png").replace("\\", "/")
        B2_pressed = os.path.join(self.f_path, "visuals/Button2_pressed.png").replace("\\", "/")
        self.V_check = os.path.join(self.f_path, "visuals/icons/confirm.png")
        self.V_cancel = os.path.join(self.f_path, "visuals/icons/cancel.png")
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Main interface")
        self.setWindowFlags(Qt.FramelessWindowHint)  # remove window border
        self.setAttribute(Qt.WA_TranslucentBackground)  # transparent background
        Ph = int((config.scale-0.45)*200); Pw = int((config.scale-0.40)*150) # window position
        Wh = int(config.scale*550); Ww = int(config.scale*400) # window size
        self.setGeometry(Ph, Pw, Wh, Ww)
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        background_top_path = os.path.join(self.f_path, "visuals/H_background1.png")
        background_bottom_path = os.path.join(self.f_path, "visuals/H1_bb.png")
        top_pixmap = QPixmap(background_top_path).scaled(
            self.width(), self.height(), 
            Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        bottom_pixmap = QPixmap(background_bottom_path).scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        composed_image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        composed_image.fill(Qt.transparent)

        # Overlay backgrounds
        painter = QPainter(composed_image)
        painter.setOpacity(config.transbckg)
        painter.drawPixmap(0, 0, bottom_pixmap)
        painter.setOpacity(1.0)
        painter.drawPixmap(0, 0, top_pixmap)
        painter.end()

        # Convert back to QPixmap and apply to label
        pixmap = QPixmap.fromImage(composed_image)
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
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(int(config.scale*45), int(config.scale*55),
                                       int(config.scale*50), int(config.scale*45)) # L, Up, R, Down
        central_widget.setLayout(main_layout)

        # Create a vertical layout for buttons on the left
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_container.setLayout(button_layout)
        button_container.setMinimumWidth(int(config.scale * 150))
        main_layout.addWidget(button_container, alignment=Qt.AlignLeft)

        #--------------------------------
        button_stylesheet =f"""
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
        """
        # VS Code Button
        open_vscode_button = QtWidgets.QPushButton("CODE")
        open_vscode_button.setMinimumSize(128, 64)
        open_vscode_button.setMaximumSize(128, 64)
        open_vscode_button.setStyleSheet(button_stylesheet)
        open_vscode_button.clicked.connect(self.open_vscode)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        open_vscode_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(open_vscode_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # SSH connection to Raspberry PI
        ssh_button = QtWidgets.QPushButton("HOST", self)
        ssh_button.setMinimumSize(128, 64)
        ssh_button.setMaximumSize(128, 64)
        ssh_button.setStyleSheet(button_stylesheet)
        ssh_button.clicked.connect(self.ssh_to_rpi)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        ssh_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(ssh_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # Cyberspace button
        cyberspace_button = QtWidgets.QPushButton("DECK", self)
        cyberspace_button.setMinimumSize(128, 64)
        cyberspace_button.setMaximumSize(128, 64)
        cyberspace_button.setStyleSheet(button_stylesheet)
        cyberspace_button.clicked.connect(self.open_cyberspace)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        cyberspace_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(cyberspace_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # Radio buttons
        hbox_container = QWidget()
        radio_layout = QHBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_main = QRadioButton("R")
        self.radio_main.setChecked(True)
        self.radio_one = QRadioButton("M")
        self.radio_two = QRadioButton("S")
        hbox_container.setLayout(radio_layout)
        hbox_container.setFixedSize(128, 64)
        r_style = """
        QRadioButton {
            color: hotpink;
            font-weight: bold;
        }
        QRadioButton::indicator {
            width: 12px;
            height: 12px;
            border-radius: 6px;
            border: 2px solid gray;
            background: white;
        }
        QRadioButton::indicator:checked {
            background: purple;
            border: 2px solid hotpink;
        }
        """
        hbox_container.setStyleSheet(r_style)

        group = QButtonGroup(self)
        group.addButton(self.radio_main)
        group.addButton(self.radio_one)
        group.addButton(self.radio_two)

        # Add to layout
        radio_layout.addWidget(self.radio_main)
        radio_layout.addWidget(self.radio_one)
        radio_layout.addWidget(self.radio_two)
        button_layout.addWidget(hbox_container, alignment=Qt.AlignCenter)
        #--------------------------------

        # Temperature stats
        self.temp_stats = TransparentImageWidget(button_layout.sizeHint(),
                                                 os.path.join(self.f_path,"visuals/nightsky.png"),
                                                 self.f_path)
        button_layout.addWidget(self.temp_stats)
        button_layout.setAlignment(Qt.AlignHCenter)
        button_layout.addStretch()
        #--------------------------------

        # Create a vertical layout for the list on the right
        list_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
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
        #--------------------------------
        
        # Ensure the app works as intended
        self.read_list()
        self.adjust_close_button_position()
        self.close_button.raise_()
        self.coords = self.init_class.get_geostats()
        self.suntime = self.init_class.daytime_calculator(self.coords[0], self.coords[1], self.today)
        self.update_weather()

        # Start other app windows
        self.start_chats()
        self.open_info_panel()
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
    def mousePressEvent(self, event):
        """
        move event logic for entire window
        """
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    # mouse drag ^
    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
    # mouse release ^
    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()
    # send to other windows ^
    def moveEvent(self, event):
        dPoint = event.pos() - event.oldPos()
        self.speechbot.move(self.speechbot.pos() + dPoint)
        self.chatbot.move(self.chatbot.pos() + dPoint)
        self.info_panel.move(self.info_panel.pos() + dPoint)
        super().moveEvent(event)
    #--------------------------------
    def open_vscode(self):
        folder_path = "C:/John"
        subprocess.Popen(["code", folder_path], shell=True)
    #--------------------------------
    def open_info_panel(self):
        """
        open info panel
        """
        self.info_panel = MainWindow()
        self.info_panel.show()
    #--------------------------------
    def start_chats(self):
        """
        open chat AIs
        """
        self.chatbot = Chatbot(main_window=self)
        self.chatbot.show()

        self.speechbot = Speechbot(main_window=self)
        self.speechbot.show()
    #--------------------------------
    def ssh_to_rpi(self):
        """
        connect to Raspberry PI
        """
        subprocess.Popen(["start", "cmd", "/k", "ssh raspberrypi"], shell=True)
    #--------------------------------
    def open_cyberspace(self):
        """
        open cyberspace from its directory
        """
        subprocess.Popen(config.cyberspace, shell=True)
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
        row_widget = QWidget()
        row_layout = QHBoxLayout()
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
            try:
                new_weath = self.get_weather_from_open_meteo(self.coords[0], self.coords[1])
                self.temp_stats.text_field.setText(
                    f"{new_weath['temperature']}°C\n"
                    f"{self.wind_description(new_weath['wind_speed'])}\n"
                    f"{self.coords[2]}"
                )
                self.temp_stats.text_field.setAlignment(Qt.AlignmentFlag.AlignBottom)
            except Exception as e:
                print(f"Weather fetch failed: {e}")
    # sub-function ^
    def wind_description(self, speed_mps):
        """
        convert wind speed to description
        """
        thresholds = [0.5, 1.6, 5.5, 10.8]
        labels = ["calm", "light air", "breezy", "windy", "stormy"]

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
