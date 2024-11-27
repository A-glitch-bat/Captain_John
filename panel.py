#--------------------------------

# Imports
import sys
import subprocess
import os
import psutil
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageDraw
import config
#--------------------------------

class InfoPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)
        self.setGeometry(int(config.scale*775), int(config.scale*225),  # W pos, H pos,
                         int(config.scale*250), int(config.scale*300))  # W size, H size
        self.setWindowTitle("INFO")
        
        # Outer frame as a border
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.setSpacing(0)

        outline_frame = QtWidgets.QFrame(self)
        outline_frame.setStyleSheet("background-color: hotpink; border-radius: 10px;")
        outer_layout.addWidget(outline_frame)

        # Inner content frame
        content_layout = QtWidgets.QVBoxLayout(outline_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.content_frame = QtWidgets.QFrame(outline_frame)
        self.content_frame.setStyleSheet("background-color: #1a1a1a; border-radius: 8px;")
        content_layout.addWidget(self.content_frame)

        # Custom title bar with close button
        title_bar = QtWidgets.QHBoxLayout()
        self.content_frame.setLayout(QtWidgets.QVBoxLayout())
        self.content_frame.layout().addLayout(title_bar)

        title_label = QtWidgets.QLabel("System Info")
        title_label.setStyleSheet("color: cyan; font: bold 10pt OCR A Extended;")
        title_bar.addWidget(title_label)
        title_bar.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        close_button = QtWidgets.QPushButton("EXIT")
        close_button.setStyleSheet("""
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
        close_button.clicked.connect(self.close_panel)
        title_bar.addWidget(close_button)

        # Draggable title bar
        title_bar.addStretch()
        title_label.mousePressEvent = self.start_move
        title_label.mouseMoveEvent = self.on_motion
        #--------------------------------
        self.central_widget = QtWidgets.QWidget()

        # CPU and RAM usage displays
        self.CPU_widget = PercentageCircleWidget(10, "CPU")
        self.RAM_widget = PercentageCircleWidget(50, "RAM")
        self.content_frame.layout().addWidget(self.CPU_widget)
        self.content_frame.layout().addWidget(self.RAM_widget)

        # Timer to update displays
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)  # Update every second

    # Functions
    #--------------------------------
    def update_usage(self):
        """
        constantly updated CPU and RAM usage displays
        """
        cpu_percent = psutil.cpu_percent(interval=0)

        if self.CPU_widget:
            # remove the previous and add the updated widget
            old_widget = self.content_frame.layout().takeAt(self.content_frame.layout().indexOf(self.CPU_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            self.CPU_widget = PercentageCircleWidget(cpu_percent, "CPU")
            self.content_frame.layout().addWidget(self.CPU_widget)

        ram_percent = psutil.virtual_memory().percent

        if self.RAM_widget:
            # remove the previous and add the updated widget
            old_widget = self.content_frame.layout().takeAt(self.content_frame.layout().indexOf(self.RAM_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            self.RAM_widget = PercentageCircleWidget(ram_percent, "RAM")
            self.content_frame.layout().addWidget(self.RAM_widget)
    #--------------------------------
    def start_move(self, event):
        """
        draggable window logic when moved
        """
        self.click_position = event.globalPos()
    # same purpose ^
    def on_motion(self, event):
        """
        draggable window logic on motion
        """
        delta = event.globalPos() - self.click_position
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.click_position = event.globalPos()
    #--------------------------------
    def close_panel(self):
        """
        stop timer on closing
        """
        self.timer.stop()
        self.close()
#--------------------------------

class PercentageCircleWidget(QtWidgets.QWidget):
    def __init__(self, percentage, name, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.name = name
        self.setMinimumSize(50, 50)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing) # smooth edges

        rect = self.rect()  # Get the rectangle representing the widget's size
        radius = min(rect.width(), rect.height()) // 2 - 10  # Calculate radius for the circle
        center = rect.center()

        # Draw arc and text
        painter.setPen(QtGui.QPen(QtGui.QColor("#FF69B4"), 16)) # colour & thickness
        span_angle = int(360 * 16 * (self.percentage / 100))
        painter.drawArc(
            center.x() - radius, center.y() - radius, int(2.15*radius), int(2.15*radius), 90 * 16, -span_angle
        )
        painter.setPen(QtGui.QColor("#FF69B4")) # colour
        painter.setFont(QtGui.QFont("OCR A Extended", 10, QtGui.QFont.Bold)) # text properties
        text = f"{self.name + ':' + str(self.percentage)}%"
        painter.drawText(rect, QtCore.Qt.AlignCenter, text)

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = InfoPanel()
    window.show()
    app.exec_()
