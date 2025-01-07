#--------------------------------

# Imports
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
#--------------------------------

# Percentage display circle widgt
#--------------------------------
class PercentageCircleWidget(QWidget):
    def __init__(self, percentage, name, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.name = name
        self.setMinimumSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # smooth edges

        rect = self.rect()  # Get the rectangle representing the widget's size
        radius = min(rect.width(), rect.height()) // 2 - 10  # Calculate radius for the circle
        center = rect.center()

        # Draw arc and text
        painter.setPen(QPen(QColor("#FF69B4"), 16)) # colour & thickness
        span_angle = int(360 * 16 * (self.percentage / 100))
        painter.drawArc(
            center.x() - radius, center.y() - radius, int(2.15*radius), int(2.15*radius), 90 * 16, -span_angle
        )
        painter.setPen(QColor("#FF69B4")) # colour
        painter.setFont(QFont("OCR A Extended", 10, QFont.Bold)) # text properties
        text = f"{self.name + ':' + str(self.percentage)}%"
        painter.drawText(rect, QtCore.Qt.AlignCenter, text)
#--------------------------------

# Percentage display bar widgt
#--------------------------------
class PercentageBarWidget(QWidget):
    def __init__(self, total, used, name, parent=None):
        super().__init__(parent)
        self.max = int(total)
        self.use = int(used)
        self.remain = self.max - self.use
        self.name = name
        self.setMinimumSize(50, 50)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # smooth edges
        rect = self.rect() # rectangle representing the widget's size
        center = rect.center()

        # Draw lines and text
        painter.setPen(QPen(QColor(255, 105, 180, 100), 24))
        painter.drawLine(int(1*center.x()/4), center.y(), int(7*center.x()/4), center.y())
        painter.setPen(QPen(QColor(255, 105, 180, 255), 24))
        painter.drawLine(int(1*center.x()/4), center.y(), int((7*self.use/self.max)*center.x()/4), center.y())

        painter.setPen(QColor("#000000")) # colour
        painter.setFont(QFont("OCR A Extended", 10, QFont.Bold)) # text properties
        text = f"{str(self.remain)+self.name +'/'+ str(self.max)+self.name} REMAINING"
        painter.drawText(rect, QtCore.Qt.AlignCenter, text)
#--------------------------------
