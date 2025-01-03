#--------------------------------

# Imports
import psutil
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QBrush, QPainterPath, QPainter

from elements.ratio_widgets import PercentageCircleWidget
import config
#--------------------------------

# Classes for separate parts of an L-shaped panel component
#--------------------------------
class TopInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("INFO_1")
        
        # Outer frame as a border
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.setSpacing(0)

        outline_frame = QFrame(self)
        outer_layout.addWidget(outline_frame)

        # Inner content frame
        content_layout = QVBoxLayout(outline_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.content_frame = QFrame(outline_frame)
        content_layout.addWidget(self.content_frame)

        # Custom title bar with close button
        title_bar = QHBoxLayout()
        self.content_frame.setLayout(QVBoxLayout())
        self.content_frame.layout().addLayout(title_bar)

        title_label = QLabel("System Info")
        title_label.setStyleSheet("color: cyan; font: bold 10pt OCR A Extended;")
        title_bar.addWidget(title_label)
        title_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Draggable title bar
        title_bar.addStretch()
        title_label.mousePressEvent = self.start_move
        title_label.mouseMoveEvent = self.on_motion
        #--------------------------------
        self.central_widget = QWidget()

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
    def paintEvent(self, event):
        """
        paint event for holographic visuals
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # custom outline of the top panel
        path = QPainterPath()
        rect = self.rect()
        radius = 30
        path.moveTo(rect.x() + radius, rect.y()) # start at top-left corner
        path.lineTo(rect.right() - radius, rect.y()) # top edge
        path.lineTo(rect.right(), rect.y() + radius) # top-right corner
        path.lineTo(rect.right(), rect.bottom()) # right edge
        path.lineTo(rect.x() + radius, rect.bottom()) # bottom edge
        path.lineTo(rect.x(), rect.bottom() - radius) # bottom-left corner 
        path.lineTo(rect.x(), rect.y() + radius) # left edge
        path.lineTo(rect.x() + radius, rect.y()) # top-left corner 

        # translucent background
        painter.setBrush(QBrush(QColor(255, 105, 180, 50)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(path)
        
        painter.end()
    #--------------------------------
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.close()
#--------------------------------

class BottomInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("INFO_2")
        
        # Outer frame as a border
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.setSpacing(0)

        outline_frame = QFrame(self)
        outer_layout.addWidget(outline_frame)

        # Inner content frame
        content_layout = QVBoxLayout(outline_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.content_frame = QFrame(outline_frame)
        content_layout.addWidget(self.content_frame)

        # Custom title bar with close button
        title_bar = QHBoxLayout()
        self.content_frame.setLayout(QVBoxLayout())
        self.content_frame.layout().addLayout(title_bar)

        title_label = QLabel("Info Sub-panel")
        title_label.setStyleSheet("color: cyan; font: bold 10pt OCR A Extended;")
        title_bar.addWidget(title_label)
        title_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        #--------------------------------
        # Draggable title bar
        title_bar.addStretch()
        #--------------------------------
        # Timer to update displays
        self.timer = QtCore.QTimer()
        self.timer.start(1000)  # Update every second
        #--------------------------------

    # Functions
    #--------------------------------
    def paintEvent(self, event):
        """
        paint event for holographic visuals
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # custom outline of the top panel
        path = QPainterPath()
        rect = self.rect()
        radius = 30
        path.moveTo(rect.x(), rect.y()) # start at top-left corner
        path.lineTo(rect.right(), rect.y()) # top edge
        path.lineTo(rect.right(), rect.bottom() - radius) # right edge
        path.lineTo(rect.right() - radius, rect.bottom()) # bottom-right corner 
        path.lineTo(rect.x() + radius, rect.bottom()) # bottom edge
        path.lineTo(rect.x(), rect.bottom() - radius) # bottom-left corner 
        path.lineTo(rect.x(), rect.y()) # left edge

        # translucent background
        painter.setBrush(QBrush(QColor(255, 105, 180, 50)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(path)
        
        painter.end()
    #--------------------------------
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.close()
#--------------------------------

# Main window class and file main
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setGeometry(int(config.scale*550) + int((config.scale-0.45)*200), # W pos,
                         int((config.scale-0.40)*150), # H pos,
                         int(config.scale*350), int(config.scale*800))  # W size, H size
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.75)

    def init_ui(self):
        """
        Setup UI with top and bottom panels, and overlay EXIT button.
        """
        # Panels
        self.top_panel = TopInfoPanel()
        self.bottom_panel = BottomInfoPanel()

        # Main layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Add top panel
        main_layout.addWidget(self.top_panel)

        # Bottom panel in a horizontal layout with spacer
        bottom_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        bottom_layout.addItem(horizontal_spacer)
        bottom_layout.addWidget(self.bottom_panel)
        main_layout.addLayout(bottom_layout)

        # Add EXIT button (overlaid on top_panel)
        self.exit_button = QPushButton("EXIT", self)
        self.exit_button.setStyleSheet("""
            QPushButton {
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
        self.exit_button.setFixedSize(70, 30)
        self.exit_button.clicked.connect(self.close)

        # Ensure the button is raised and positioned
        self.reposition_exit_button()
#--------------------------------
    def resizeEvent(self, event):
        """
        Reposition the EXIT button when the window is resized.
        """
        self.reposition_exit_button()
        super().resizeEvent(event)
#--------------------------------
    def reposition_exit_button(self):
        """
        Dynamically position the EXIT button at the top-right corner of the `top_panel`.
        """
        if self.top_panel:
            top_panel_geometry = self.top_panel.geometry()
            self.exit_button.setGeometry(
                QRect(
                    top_panel_geometry.x() + top_panel_geometry.width() - self.exit_button.width() - 25,
                    top_panel_geometry.y() + 25,
                    self.exit_button.width(),
                    self.exit_button.height(),
                )
            )
#--------------------------------
    def closeEvent(self, _):
        """
        shut down both timers and close app
        """
        self.top_panel.stop_timer()
        self.bottom_panel.stop_timer()
        self.close()
#--------------------------------

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
#--------------------------------