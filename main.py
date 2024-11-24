#--------------------------------

# Imports
import sys
import subprocess
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import config
from panel import InfoPanel
from aihead import AIhead
from listmaker import ListMaker
#--------------------------------

# Main class
class CustomWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up the main window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # transparent background
        self.setGeometry(200, 150, config.scale*550, config.scale*400)  # window size and position
        #--------------------------------

        # Load and set the custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_h.png")
        pixmap = QtGui.QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        
        # Create the custom "X" close button
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
        self.close_button.clicked.connect(self.close)  # Connect to the close function
        
        # Create a central widget to hold the layout for the other buttons
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # Main horizontal layout for the button column and terminal display
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(config.scale*25, config.scale*75, config.scale*50, config.scale*75) # L, Up, R, Down
        central_widget.setLayout(main_layout)

        # Create a vertical layout for buttons on the left
        button_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(button_layout)  # Add button column to main layout
        #--------------------------------

        # Buttons
        B1 = os.path.join(config.destination, "Button1.png")
        B1_pressed = os.path.join(config.destination, "Button1.png")
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
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
        button_layout.addWidget(open_vscode_button)
        #--------------------------------
        # Info Butoon
        self.print_button = QtWidgets.QPushButton("INFO", self)
        self.print_button.setMinimumSize(128, 64)
        self.print_button.setMaximumSize(128, 64)
        self.print_button.setStyleSheet(f"""
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
        self.print_button.clicked.connect(self.open_info_panel)
        button_layout.addWidget(self.print_button)
        #--------------------------------
        # AI start button
        AI_button = QtWidgets.QPushButton("CHAT", self)
        AI_button.setMinimumSize(128, 64)
        AI_button.setMaximumSize(128, 64)
        AI_button.setStyleSheet(f"""
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
        AI_button.clicked.connect(self.start_AI)
        button_layout.addWidget(AI_button)
        #--------------------------------
        # Listmaker button
        list_button = QtWidgets.QPushButton("LIST", self)
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
        list_button.clicked.connect(self.start_listdisplay)
        button_layout.addWidget(list_button)
        #--------------------------------
        # Stretchable space to push buttons to the top
        button_layout.addStretch()
        #--------------------------------

        # Terminal display
        self.terminal_display = QtWidgets.QTextEdit(self)
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        self.terminal_display.setMinimumSize(config.scale*128, config.scale*64)
        self.terminal_display.setMaximumSize(config.scale*256, config.scale*128)
        main_layout.addWidget(self.terminal_display)
        #--------------------------------
        # Ensure the app can be closed
        self.adjust_close_button_position()
        self.close_button.raise_()
    #--------------------------------

    # Functions
    #--------------------------------
    def adjust_close_button_position(self):
        # Position close button in the top-right corner based on current window width
        self.close_button.setGeometry(self.width() - 60, 25, 50, 25)
    #--------------------------------
    def open_vscode(self):
        folder_path = "C:/John"
        subprocess.Popen(["code", folder_path], shell=True)
    #--------------------------------
    def open_info_panel(self):
        # Open InfoPanel on button click
        self.info_panel = InfoPanel() # prevent garbage-collection
        self.info_panel.show()
    #--------------------------------
    def start_AI(self):
        # Open AI head on button click
        self.aihead = AIhead() # prevent garbage-collection
        self.aihead.show()
    #--------------------------------
    def start_listdisplay(self):
        # Open list display on button click
        self.listdisplay = ListMaker() # prevent garbage-collection
        self.listdisplay.show()
    #--------------------------------

#--------------------------------
# Wake John up
app = QtWidgets.QApplication(sys.argv)
window = CustomWindow()
window.show()
sys.exit(app.exec_())
#--------------------------------
