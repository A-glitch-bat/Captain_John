#--------------------------------

# Imports
import sys
import subprocess
import os
import psutil
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageDraw
#--------------------------------

class InfoPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(50, 450, 300, 300)
        self.setWindowTitle("INFO")
        
        # Outer frame as a border
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        outer_layout.setSpacing(0)

        outline_frame = QtWidgets.QFrame(self)
        outline_frame.setStyleSheet("background-color: hotpink; border-radius: 10px;")
        outer_layout.addWidget(outline_frame)

        # Inner frame for content
        content_layout = QtWidgets.QVBoxLayout(outline_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        content_frame = QtWidgets.QFrame(outline_frame)
        content_frame.setStyleSheet("background-color: #1a1a1a; border-radius: 8px;")
        content_layout.addWidget(content_frame)

        # Custom title bar with close button
        title_bar = QtWidgets.QHBoxLayout()
        content_frame.setLayout(QtWidgets.QVBoxLayout())
        content_frame.layout().addLayout(title_bar)

        title_label = QtWidgets.QLabel("System Info")
        title_label.setStyleSheet("color: hotpink; font: bold 10pt OCR A Extended;")
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
                background-color: #333333;  /* Slightly darker on hover */
            }
            QPushButton:pressed {
                background-color: #555555;  /* Even darker on press */
            }
        """)
        close_button.clicked.connect(self.close_panel)
        title_bar.addWidget(close_button)

        # Draggable title bar
        title_bar.addStretch()
        title_label.mousePressEvent = self.start_move
        title_label.mouseMoveEvent = self.on_motion
        #--------------------------------

        # CPU and RAM usage displays
        self.cpu_label = QtWidgets.QLabel("CPU: --%")
        self.ram_label = QtWidgets.QLabel("RAM: --%")
        for label in (self.cpu_label, self.ram_label):
            label.setStyleSheet("color: magenta; font: bold 10pt OCR A Extended;")
            content_frame.layout().addWidget(label)

        # Drawing area for CPU and RAM usage arcs
        self.cpu_canvas = QtWidgets.QLabel()
        self.cpu_canvas.setFixedSize(100, 100)
        self.ram_canvas = QtWidgets.QLabel()
        self.ram_canvas.setFixedSize(100, 100)
        content_frame.layout().addWidget(self.cpu_canvas)
        content_frame.layout().addWidget(self.ram_canvas)

        # Set up a timer to update the CPU and RAM usage every second
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)  # Update every 1000 ms (1 second)

    def update_usage(self):
        # Update CPU and RAM usage data and display
        cpu_percent = psutil.cpu_percent(interval=0)
        ram_percent = psutil.virtual_memory().percent
        self.cpu_label.setText(f"CPU: {cpu_percent}%")
        self.ram_label.setText(f"RAM: {ram_percent}%")
        self.draw_arc(self.cpu_canvas, cpu_percent, "hotpink")
        self.draw_arc(self.ram_canvas, ram_percent, "hotpink")

    # Draw arcs for usage percentages
    def draw_arc(self, label, percent, color):
        pixmap = QtGui.QPixmap(100, 100)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidth(8)
        painter.setPen(pen)
        painter.drawArc(10, 10, 80, 80, 90 * 16, -int(percent * 3.6) * 16)
        painter.end()
        label.setPixmap(pixmap)

    # Draggable window logic
    def start_move(self, event):
        self.click_position = event.globalPos()

    def on_motion(self, event):
        delta = event.globalPos() - self.click_position
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.click_position = event.globalPos()

    # Clean up the timer when closing the panel
    def close_panel(self):
        self.timer.stop()  # Stop the timer
        self.close()
#--------------------------------
