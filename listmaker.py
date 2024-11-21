from PyQt5 import QtWidgets, QtGui, QtCore
import os
import torch
import config
#--------------------------------

# List interaction class
class ListMaker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Base for list component")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # transparent background
        self.setGeometry(125, 550, int(config.scale*450), int(config.scale*300)) # window size and position
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_h.png")
        pixmap = QtGui.QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        
        # Create close button
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
        #--------------------------------
        # Buttons and widgets
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        V_check = os.path.join(config.destination, "Vibe_check.png")
        V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
        #--------------------------------

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(int(config.scale*50), int(config.scale*75),
                                       int(config.scale*50), int(config.scale*75)) # L, Up, R, Down
        input_layout = QtWidgets.QHBoxLayout()

        # Input
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("add to list")
        self.input_field.returnPressed.connect(self.write_input)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.setIcon(QtGui.QIcon.fromTheme(V_check))
        self.submit_button.setFixedSize(30, 30)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 2px solid hotpink;
            }
        """)
        self.submit_button.clicked.connect(self.write_input)
        
        input_layout.addWidget(self.submit_button)
        main_layout.addLayout(input_layout)

        # Output
        self.output_display = QtWidgets.QTextEdit(self)
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        
        main_layout.addWidget(self.output_display)
        self.setLayout(main_layout)
        #--------------------------------
        # Ensure the app works as intended
        self.read_list()
        self.adjust_close_button_position()
        self.close_button.raise_()
    #--------------------------------

    # Functions
    #--------------------------------
    def adjust_close_button_position(self):
        # Position close button in the top-right corner based on current window width
        self.close_button.setGeometry(self.width() - 60, 25, 50, 25)
    #--------------------------------
    def append_text(self, file_path, text):
        with open(file_path, "a+") as file:
            file.seek(0, 2)  # Move the pointer to the end of the file
            if file.tell() > 0:  # Check if the file is not empty
                file.seek(file.tell() - 1)  # Move to the last character
                last_char = file.read(1)
                if last_char != "\n":  # If the last character isn't a newline
                    file.write("\n")
            file.write(text)
    #--------------------------------
    def write_input(self):
        input_text = self.input_field.text()
        if input_text: # input exists
            self.append_text("list.txt", input_text)
            self.input_field.clear() #clear
            self.read_list()
    #--------------------------------
    def read_list(self):
        try:
            with open("list.txt", "r") as file:
                lines = file.readlines()
            self.output_display.clear()
            self.output_display.append("".join(lines))
        except FileNotFoundError:
            self.output_display.clear()
            self.output_display.append("Error: 'list.txt' not found.")
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ListMaker()
    window.show()
    app.exec_()
