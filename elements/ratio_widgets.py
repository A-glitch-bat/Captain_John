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
    def __init__(self, percentage, name, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.name = name
        self.setMinimumSize(50, 50)
