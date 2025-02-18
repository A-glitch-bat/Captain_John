#--------------------------------

# Imports
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTextEdit, QStackedLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint
#--------------------------------

# Transparent image widget ft. a very clear naming system
class TransparentImageWidget(QWidget):
    def __init__(self, geometry, image_path):
        super(TransparentImageWidget, self).__init__()

        # prepare image as pixmap
        pixmap = QPixmap(image_path)
        transparent_pixmap = self.make_transparent(pixmap, 75)

        # QLabel for background image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(transparent_pixmap)
        H = geometry.height();W = geometry.width()
        self.image_label.setMaximumSize(H+50, W+50) # size limit

        # text field
        self.text_field = QTextEdit(self)
        self.text_field.setReadOnly(True)
        self.text_field.setAttribute(Qt.WA_TranslucentBackground, True)
        self.text_field.setMaximumSize(H+50, W+50) # size limit
        self.text_field.setText("Weather info")
        self.text_field.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0);  
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 4px black;
                padding: 10px;  
                padding-top: 50px;
            }
        """)
        self.text_field.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Stack text on top of image
        stacked_layout = QStackedLayout()
        stacked_layout.addWidget(self.text_field)
        stacked_layout.addWidget(self.image_label)
        stacked_layout.setStackingMode(QStackedLayout.StackAll)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)

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