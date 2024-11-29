from PyQt5 import QtWidgets, QtGui, QtCore
import os
import torch
import config
#--------------------------------

# List interaction class
class TtS(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Base for list component")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # transparent background
        self.setGeometry(int(config.scale*200), int(config.scale*550), 
                         int(config.scale*350), int(config.scale*450))  # window size, window position
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_v.png")
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
        self.txt_file = config.txt_file
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        self.V_check = os.path.join(config.destination, "Vibe_check.png")
        self.V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
        #--------------------------------

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(int(config.scale*50), int(config.scale*75),
                                       int(config.scale*50), int(config.scale*75)) # L, Up, R, Down
        #--------------------------------
        # Ensure the app works as intended
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

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TtS()
    window.show()
    app.exec_()
