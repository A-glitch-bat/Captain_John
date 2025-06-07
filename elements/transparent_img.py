#--------------------------------

# Imports
import os

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTextEdit, QStackedLayout
from PyQt5.QtGui import QPixmap, QPainter, QPixmap, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QRectF
import config
#--------------------------------

# Transparent image widget ft. a very clear naming system
class TransparentImageWidget(QWidget):
    def __init__(self, geometry, image_path):
        super(TransparentImageWidget, self).__init__()
        """
        prepare a layered widget for weather status display
        """
        self.png_daytime = os.path.join(config.destination, "icons/pixel_sun.png")
        self.png_nighttime = os.path.join(config.destination, "icons/pixel_moon.png")
        self.overlay_text = "Weather"

        # QWidget size
        column_W = geometry.width()
        self.setFixedSize(column_W+100, column_W-25)

        # Background image
        self.bg_label = QLabel(self)
        bg_pixmap = QPixmap(image_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        transparent_pixmap = self.make_transparent(bg_pixmap, 200)
        self.bg_label.setPixmap(transparent_pixmap)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

        # --- Overlay Text (Left side) ---
        self.text_field = QTextEdit(self)
        self.text_field.setText(self.overlay_text)
        self.text_field.setStyleSheet("""
                QTextEdit {
                    background-color: rgba(0, 0, 0, 0);  
                    color: hotpink;
                    font-family: OCR A Extended;
                    font-size: 14px;
                    border: 4px black;
                    padding: 10px;
                    padding-top: 25px;
                }                 
            """)
        self.text_field.setGeometry(10, 20, self.width() // 2 + 10, self.height() - 25)

        # Layout
        self.image_container = QWidget(self)
        self.image_container.setAttribute(Qt.WA_TranslucentBackground)
        self.image_container.setFixedSize(self.width() // 2, self.height() // 2)

        layout = QVBoxLayout(self.image_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Daytime/nighttime png with subtext
        image_label = QLabel()
        pixmap = QPixmap(self.png_nighttime).scaled(self.image_container.width(),
                                                    self.image_container.height()-25,
                                                    Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        caption_label = QLabel("Sunrise\ntime")
        caption_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 0, 0, 0);  
                    color: hotpink;
                    background: transparent;
                    font-family: OCR A Extended;
                    font-size: 14px;
                }
            """)
        caption_label.setAlignment(Qt.AlignCenter)

        # Add to layout and reposition
        layout.addWidget(image_label)
        layout.addWidget(caption_label)
        self.image_container.move(self.width() - self.image_container.width(),
                                  self.height() // 2 - self.image_container.height() // 2)

    # Functions
    def make_transparent(self, pixmap, opacity):
        """
        alter pixmap opacity
        """
        transparent = QPixmap(pixmap.size())
        transparent.fill(Qt.GlobalColor.transparent)

        # main image
        painter = QPainter(transparent)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(opacity / 255)
        radius = 15
        path = QPainterPath()
        path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)

        # rounded border
        pen = QPen(QColor("hotpink"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(QRectF(0, 0, pixmap.width(), pixmap.height()), radius, radius)

        painter.end()

        return transparent
#--------------------------------