#--------------------------------

# Imports
import random
import config
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QFont, QBrush, QColor, QPixmap, QIcon
from PyQt5.QtCore import QTimer
#--------------------------------

# Digital rain widget class
class DigitalRainPanel(QtWidgets.QWidget):
    def __init__(self, sizingVect, colourVect, parent=None):
        super().__init__(parent)
        self.timer_interval = 100
        self.font_size = 12
        self.setGeometry(sizingVect[0]-125, sizingVect[1]-100, # window size
                         sizingVect[2]-125, sizingVect[3]-100) # window position
        self.colourVect = colourVect
        self.font = QFont("OCR A Extended", self.font_size, QFont.Bold)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rain)
        self.timer.start(self.timer_interval)

        # Randomly initialize rain matirx
        self.columns = []
        num_columns = self.width() // self.font_size
        for _ in range(num_columns):
            self.columns.append(random.randint(-45, 0))

    # Functions
    #--------------------------------
    def update_rain(self):
        """
        timed update function
        """
        self.columns = [y + 1 if y < self.height() // self.font_size else -5 for y in self.columns]
        self.update() # trigger event
    # sub-function ^
    def paintEvent(self, event):
        """
        paint the rain matrix onto widget
        """
        painter = QPainter(self)
        painter.setFont(self.font)

        num_columns = len(self.columns)
        for MrIterator in range(num_columns):
            x = MrIterator * self.font_size
            y = self.columns[MrIterator] * self.font_size

            if y > 0:
                color = QColor(self.colourVect[0], self.colourVect[1], self.colourVect[2], 100) # character trail
                painter.setPen(color)
                for MrJterator in range(y // self.font_size - 5, y // self.font_size):
                    if MrJterator >= 0:
                        painter.drawText(x, MrJterator * self.font_size, random.choice("01"))

            if y >= 0:
                color = QColor(self.colourVect[0], self.colourVect[1], self.colourVect[2]) # first character
                painter.setPen(color)
                painter.drawText(x, y, random.choice("01DCGHBMKWQOIJ"))

        painter.end()
#--------------------------------
