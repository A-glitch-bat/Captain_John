#--------------------------------

# Imports
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint
#--------------------------------

# Transparent image widget ft. a very clear naming system
class TransparentImageWidget(QWidget):
    def __init__(self, geometry, image_path):
        super().__init__()

        # prepare image as pixmap
        pixmap = QPixmap(image_path)
        transparent_pixmap = self.make_transparent(pixmap, 75)

        # QLabel for background image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(transparent_pixmap)
        H = geometry.height();W = geometry.width()
        self.image_label.setMaximumSize(H+50, W+50) # size limit

        # QLabel for overlay text
        self.text_label = QLabel("Overlay Text", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)

        # Stack text on top of image
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)
        p = self.geometry().bottomLeft()
        self.text_label.move(p)
        self.setLayout(layout)
        #--------------------------------

    # Functions
    def make_transparent(self, pixmap, opacity):
        """
        alter pixmap opacity
        """
        transparent = QPixmap(pixmap.size())
        transparent.fill(Qt.GlobalColor.transparent)

        painter = QPainter(transparent)
        painter.setOpacity(opacity / 255)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return transparent
#--------------------------------