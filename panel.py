#--------------------------------

# Imports
import psutil
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QPalette, QPainter, QPen, QFont

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
        self.setWindowOpacity(0.8)
        self.setWindowTitle("INFO_1")
        
        # Outer frame as a border
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.setSpacing(0)

        outline_frame = QFrame(self)
        outline_frame.setStyleSheet("background-color: hotpink; border-radius: 10px;")
        outer_layout.addWidget(outline_frame)

        # Inner content frame
        content_layout = QVBoxLayout(outline_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.content_frame = QFrame(outline_frame)
        self.content_frame.setStyleSheet("background-color: #1a1a1a; border-radius: 8px;")
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
        self.setWindowOpacity(0.8)
        self.setWindowTitle("INFO_2")
        
        # Outer frame as a border
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.setSpacing(0)

        outline_frame = QFrame(self)
        outline_frame.setStyleSheet("background-color: hotpink; border-radius: 10px;")
        outer_layout.addWidget(outline_frame)

        # Inner content frame
        content_layout = QVBoxLayout(outline_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.content_frame = QFrame(outline_frame)
        self.content_frame.setStyleSheet("background-color: #1a1a1a; border-radius: 8px;")
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
        
        # Custom title bar with close button
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        outline_frame = QFrame(self)
        self.content_frame = QFrame(outline_frame)
        title_bar = QHBoxLayout()
        self.content_frame.setLayout(QVBoxLayout())
        self.content_frame.layout().addLayout(title_bar)

    def init_ui(self):
        # Create instances of TopPanel and BottomPanel
        self.top_panel = TopInfoPanel()
        self.bottom_panel = BottomInfoPanel()

        # Create spacers for alignment
        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        # Combine layouts in L-shape and add close button
        main_layout = QVBoxLayout()
        close_button = QPushButton("EXIT")
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
        close_button.clicked.connect(self.closeEvent)
        main_layout.addWidget(close_button)

        bottom_layout = QHBoxLayout()
        bottom_layout.addItem(horizontal_spacer)
        bottom_layout.addWidget(self.bottom_panel)

        main_layout.addWidget(self.top_panel)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

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