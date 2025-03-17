#--------------------------------

# Imports
import sys
import subprocess
import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer

from panel import MainWindow
from aihead import AIhead
from ttshead import TtS
from tasks.weather_api import UsageThread
from elements.digitrain import DigitalRainPanel
from elements.glitchwidget import GlitchWidget
from elements.transparent_img import TransparentImageWidget
import config
#--------------------------------

# Main class
class CustomWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
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
        # Buttons and widgets
        self.txt_file = config.txt_file
        B1 = os.path.join(config.destination, "Button1.png")
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        self.V_check = os.path.join(config.destination, "Vibe_check.png")
        self.V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
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
        self.info_button = QtWidgets.QPushButton("INFO", self)
        self.info_button.setMinimumSize(128, 64)
        self.info_button.setMaximumSize(128, 64)
        self.info_button.setStyleSheet(f"""
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
        self.info_button.clicked.connect(self.open_info_panel)
        
        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        self.info_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(self.info_button, alignment=Qt.AlignCenter)
        #--------------------------------
        # Testing button
        list_button = QtWidgets.QPushButton("TEST", self)
        list_button.setMinimumSize(128, 64)
        list_button.setMaximumSize(128, 64)
        list_button.setStyleSheet(f"""
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
        list_button.clicked.connect(self.start_ttshead)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        list_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(list_button, alignment=Qt.AlignCenter)
        #--------------------------------

        # Temperature stats
        self.temp_stats = TransparentImageWidget(button_layout.sizeHint(), os.path.join(config.destination, "skyline.png"))
        button_layout.addWidget(self.temp_stats)
        button_layout.setAlignment(Qt.AlignHCenter)
        button_layout.addStretch()
        #--------------------------------

        # Start the panels
        self.start_AI()
        self.start_ttshead()
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
        self.weather_api = UsageThread()
        self.coords = self.weather_api.get_coordinates()
        #--------------------------------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(60000)

        # Ensure the app works as intended
        self.read_list()
        self.adjust_close_button_position()
        self.close_button.raise_()
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
    def open_info_panel(self):
        """
        Open InfoPanel on button click
        """
        self.info_panel = MainWindow() # prevent garbage-collection
        self.info_panel.show()
    #--------------------------------
    def start_AI(self):
        """
        Open AI head on button click
        """
        self.aihead = AIhead() # prevent garbage-collection
        self.aihead.show()
    #--------------------------------
    def start_ttshead(self):
        """
        Open list display on button click
        """
        self.listdisplay = TtS() # prevent garbage-collection
        self.listdisplay.show()
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
    def update_weather(self):
        new_weath = self.weather_api.get_weather_from_open_meteo(self.coords[0], self.coords[1])
        self.temp_stats.text_field.setText(str(new_weath['temperature'])+"°C \n"+str(new_weath['wind_speed'])+"m/s")
        self.temp_stats.text_field.setAlignment(Qt.AlignmentFlag.AlignBottom)
    #--------------------------------

#--------------------------------
# Wake John up
app = QtWidgets.QApplication(sys.argv)
window = CustomWindow()
window.show()
sys.exit(app.exec_())
#--------------------------------
