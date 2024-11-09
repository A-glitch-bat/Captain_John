#--------------------------------

# Imports
import sys
import subprocess
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageDraw
from panel import info_panel
#--------------------------------

# Main class
class CustomWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Enable transparent background
        self.setGeometry(200, 150, 550, 400)  # Set window size and position

        # Load and set the custom background image
        self.background_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("C:/John/visuals/xmas_visuals/xmas_border_h.png")
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        
        # Create the custom "X" close button
        self.close_button = QtWidgets.QPushButton("X", self)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.close_button.clicked.connect(self.close)  # Connect to the close function
        
        # Create a central widget to hold the layout for the other buttons
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a horizontal layout for the VS Code and placeholder button
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(15)
        
        # Create a vertical layout to combine button layout and terminal display
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

        # Button to open VS Code
        open_vscode_button = QtWidgets.QPushButton("CODE")
        open_vscode_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        open_vscode_button.setMinimumSize(128, 64)
        open_vscode_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border: none;
                background-image: url('C:/John/visuals/Button1.png');
            }
            QPushButton:hover {
                background-image: url('C:/John/visuals/Button1.png');
            }
            QPushButton:pressed {
                background-image: url('C:/John/visuals/Button1.png');
            }
        """)
        open_vscode_button.clicked.connect(self.open_vscode)
        button_layout.addWidget(open_vscode_button)

        # Create a custom close button with an image
        print_button = QtWidgets.QPushButton("INFO", self)
        print_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        print_button.setMinimumSize(128, 64)
        print_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border: none;
                background-image: url('C:/John/visuals/Button1.png');
            }
            QPushButton:hover {
                background-image: url('C:/John/visuals/Button1.png');
            }
            QPushButton:pressed {
                background-image: url('C:/John/visuals/Button1.png');
            }
        """)
        print_button.clicked.connect(self.open_vscode)
        button_layout.addWidget(print_button)

        # Create a custom close button with an image
        stats_button = QtWidgets.QPushButton("PRINT", self)
        stats_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        stats_button.setMinimumSize(128, 64)
        stats_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border: none;
                background-image: url('C:/John/visuals/Button1.png');
            }
            QPushButton:hover {
                background-image: url('C:/John/visuals/Button1.png');
            }
            QPushButton:pressed {
                background-image: url('C:/John/visuals/Button1.png');
            }
        """)
        stats_button.clicked.connect(self.print_to_terminal)
        button_layout.addWidget(stats_button)

        # Create the terminal display area
        self.terminal_display = QtWidgets.QTextEdit(self)
        self.terminal_display.setReadOnly(True)  # Make it read-only
        self.terminal_display.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        self.terminal_display.setMinimumSize(128, 64)
        self.terminal_display.setMaximumSize(256, 128)
        main_layout.addWidget(self.terminal_display)
        
        # Ensure the app can be closed
        self.adjust_close_button_position()
        self.close_button.raise_()
    #--------------------------------

    # Functions
    def adjust_close_button_position(self):
        # Position close button in the top-right corner based on current window width
        self.close_button.setGeometry(self.width() - 40, 10, 30, 30)

    def open_vscode(self):
        folder_path = "C:/John"
        subprocess.Popen(["code", folder_path], shell=True)

    def print_to_terminal(self):
        # Append a test message to the terminal display
        self.terminal_display.append("This is a test message printed to the terminal.")
#--------------------------------

# Wake John up
app = QtWidgets.QApplication(sys.argv)
window = CustomWindow()
window.show()
sys.exit(app.exec_())
#--------------------------------
