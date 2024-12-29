#--------------------------------

# Imports
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QSize
#--------------------------------

# On/Off status display class
class StatusButton(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("0FF")
        self.setFixedSize(QSize(48, 48))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: hotpink;
                border: 3px solid hotpink;
                border-radius: 14px;
                font-family: OCR A Extended;
                font-size: 14px;
                font-weight: bold;
            }
        """)

    # Functions
    #--------------------------------
    def set_status(self, status):
        """
        does what it says on the tin
        """
        if not status:
            self.setText("0FF")
            self.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    color: hotpink;
                    border: 3px solid hotpink;
                    border-radius: 14px;
                    font-family: OCR A Extended;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
        else:
            self.setText("0N")
            self.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    color: cyan;
                    border: 3px solid cyan;
                    border-radius: 14px;
                    font-family: OCR A Extended;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
    #--------------------------------
