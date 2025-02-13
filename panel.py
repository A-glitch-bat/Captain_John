#--------------------------------

# Imports
import shutil
import requests
import torch

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QTextEdit, QFrame, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QBrush, QPainterPath, QPainter

from elements.glitchwidget import GlitchWidget
from elements.ratio_widgets import PercentageCircleWidget, PercentageBarWidget, HoloDataWidget
from tasks.usage_worker import UsageThread
import config
#--------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# Classes for separate parts of an L-shaped panel component
#--------------------------------
class TopInfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("INFO_1")
        
        # outer frame
        outer_layout = QVBoxLayout(self)
        outer_layout.setSpacing(0)
        outline_frame = QFrame(self)
        outer_layout.addWidget(outline_frame)

        # layout
        self.content_layout = QVBoxLayout(outline_frame)
        title_bar = QHBoxLayout()
        title_label = QLabel("INFO")
        title_label.setStyleSheet("color: hotpink; font: bold 10pt OCR A Extended;")
        title_bar.addWidget(title_label)

        # title bar
        title_bar.addStretch()
        title_label.mousePressEvent = self.start_move
        title_label.mouseMoveEvent = self.on_motion
        #--------------------------------
        self.central_widget = QWidget()

        # CPU, RAM, GPU, disk usage displays
        self.CPU_widget = PercentageCircleWidget(10, "CPU")
        self.RAM_widget = PercentageCircleWidget(50, "RAM")
        self.GPU_widget = HoloDataWidget("temp", "GPU")
        total, used, _ = shutil.disk_usage("C:/")
        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        self.space_widget = PercentageBarWidget(total_gb, used_gb, "GB")

        self.circles_layout = QHBoxLayout()
        self.stats_layout = QHBoxLayout()
        self.content_layout.addLayout(self.circles_layout)
        self.content_layout.addLayout(self.stats_layout)
        self.content_layout.addWidget(self.space_widget)

        self.stats_layout.addWidget(self.GPU_widget)
        self.circles_layout.addWidget(self.CPU_widget)
        self.circles_layout.addWidget(self.RAM_widget)

        # Background worker thread to update stats
        self.worker = UsageThread()
        self.worker.data_updated.connect(self.update_stats)
        self.worker.start()

    # Functions
    #--------------------------------
    def update_stats(self, data):
        """
        constantly update info displays
        """
        if self.GPU_widget:
            # remove the previous and add the updated widget
            old_widget = self.stats_layout.takeAt(self.stats_layout.indexOf(self.GPU_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            words = data['gpu'].rsplit(" ", 2)  # Split only the last two spaces
            disp_gpu = " ".join(words[-2:]) if len(words) >= 2 else data['gpu']
            self.GPU_widget = HoloDataWidget(disp_gpu, data['temp'])
            self.stats_layout.addWidget(self.GPU_widget)

        if self.CPU_widget:
            # remove the previous and add the updated widget
            old_widget = self.circles_layout.takeAt(self.circles_layout.indexOf(self.CPU_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            self.CPU_widget = PercentageCircleWidget(data['cpu'], "CPU")
            self.circles_layout.addWidget(self.CPU_widget)

        if self.RAM_widget:
            # remove the previous and add the updated widget
            old_widget = self.circles_layout.takeAt(self.circles_layout.indexOf(self.RAM_widget))
            if old_widget:
                old_widget.widget().deleteLater()
            self.RAM_widget = PercentageCircleWidget(data['ram'], "RAM")
            self.circles_layout.addWidget(self.RAM_widget)
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

class BottomInfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("INFO_2")
        #--------------------------------
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Text field
        self.text_field = QTextEdit(self)
        self.text_field.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0);
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: none;
            }
        """)
        self.text_field.setReadOnly(True)
        self.text_field.setAttribute(Qt.WA_TranslucentBackground, True)

        # Stack glitch over text
        glitch_overlay = GlitchWidget(self)
        stacked_layout = QStackedLayout()
        stacked_layout.addWidget(self.text_field)
        stacked_layout.addWidget(glitch_overlay)
        stacked_layout.setStackingMode(QStackedLayout.StackAll)

        glitch_container = QWidget()
        glitch_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        glitch_container.setMinimumHeight(100)
        glitch_container.setMinimumWidth(100)

        glitch_container.setLayout(stacked_layout)
        def resize_glitch():
            glitch_overlay.setGeometry(self.text_field.geometry())
        glitch_container.resizeEvent = lambda event: resize_glitch()

        main_layout.addWidget(glitch_container)
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

# Main window class and file main
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setGeometry(int(config.scale*565) + int((config.scale-0.45)*200), # W pos,
                         int((config.scale-0.40)*135), # H pos,
                         int(config.scale*450), int(config.scale*800))  # W size, H size
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.75)

    def init_ui(self):
        """
        Setup UI with top and bottom panels, and overlay EXIT button.
        """
        # create panels and layout
        self.top_panel = TopInfoPanel()
        self.bottom_panel = BottomInfoPanel()
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # add panels with a spacer on the bottom left
        main_layout.addWidget(self.top_panel)
        bottom_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(
            10, 5, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        bottom_layout.addItem(horizontal_spacer)
        bottom_layout.setStretch(0, 1)
        bottom_layout.addWidget(self.bottom_panel)
        bottom_layout.setStretch(1, 2)
        main_layout.addLayout(bottom_layout)

        # close button without own space
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
        self.reposition_exit_button()
#--------------------------------
    def resizeEvent(self, event):
        """
        reposition close button on resize
        """
        self.reposition_exit_button()
        super().resizeEvent(event)
#--------------------------------
    def reposition_exit_button(self):
        """
        position close button at the top-right corner
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
        self.close()
#--------------------------------

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
