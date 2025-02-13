#--------------------------------

# Imports
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
from PyQt5.QtCore import QTimer, Qt
#--------------------------------

# Percentage display circle widget
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
        painter.setPen(QPen(QColor(255, 105, 180, 100), 16)) # colour & thickness
        painter.drawArc(
            center.x() - radius, center.y() - radius, int(2*radius), int(2*radius), 90 * 16, -(360 * 16)
        )

        painter.setPen(QPen(QColor("#FF69B4"), 16)) # colour & thickness
        span_angle = int(360 * 16 * (self.percentage / 100))
        painter.drawArc(
            center.x() - radius, center.y() - radius, int(2*radius), int(2*radius), 90 * 16, -span_angle
        )
        painter.setPen(QColor("#FF69B4")) # colour
        painter.setFont(QFont("OCR A Extended", 10, QFont.Bold)) # text properties
        text = f"{self.name + ':' + str(self.percentage)}%"
        painter.drawText(rect, QtCore.Qt.AlignCenter, text)
#--------------------------------

# Percentage display bar widget
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

# Advanced stats display widget
#--------------------------------
class AdvDataWidget(QWidget):
    def __init__(self, label, value, parent=None):
        super().__init__(parent)
        self.label = label
        self.value = value
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 10px;")
        
        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Label for the name
        self.label_widget = QLabel(str(self.label))  # Convert to string
        self.label_widget.setFont(QFont("OCR A Extended", 14, QFont.Bold))
        self.label_widget.setStyleSheet("color: #0ff;")  # Neon cyan text

        # Value display
        self.value_widget = QLabel(self.value)
        self.value_widget.setFont(QFont("DS-Digital", 20, QFont.Bold))
        self.value_widget.setStyleSheet("color: #FF1493;")
        self.add_glow_effect(self.value_widget, QColor("#FF1493"))

        # Add widgets to layout
        layout.addWidget(self.label_widget)
        layout.addWidget(self.value_widget)
        self.setLayout(layout)

    def add_glow_effect(self, widget, color):
        """Adds a neon glow effect to a widget."""
        glow = QGraphicsDropShadowEffect()
        glow.setColor(color)
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        widget.setGraphicsEffect(glow)
#--------------------------------

# Holographic stats display widget
#--------------------------------
class HoloDataWidget(QWidget):
    def __init__(self, val1, val2, parent=None):
        super().__init__(parent)
        self.val1 = val1
        self.val2 = val2
        
        # Set layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border-radius: 10px;")

        # Label widgets
        self.label_widget = QLabel(self.val1)
        self.label_widget.setFont(QFont("OCR A Extended", 14, QFont.Bold))
        self.label_widget.setStyleSheet("color: hotpink;")
        self.value_widget = QLabel(self.val2)
        self.value_widget.setFont(QFont("OCR A Extended", 14, QFont.Bold))
        self.value_widget.setStyleSheet("color: hotpink;")

        # Add widgets to layout
        layout.addWidget(self.label_widget)
        layout.addWidget(self.value_widget)
        self.setLayout(layout)
#--------------------------------