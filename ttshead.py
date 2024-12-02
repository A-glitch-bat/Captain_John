#--------------------------------

# Imports
import os
import random
import pyttsx3
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer
import config
#--------------------------------

# List interaction class
class TtS(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Make glowy text to speech panel")
        self.setWindowFlags(Qt.FramelessWindowHint) # remove window border
        self.setAttribute(Qt.WA_TranslucentBackground) # transparent background
        self.setGeometry(int((config.scale-0.45)*200), int((config.scale-0.40)*150 + int(config.scale*400)), 
                         int(config.scale*350), int(config.scale*450))  # window size, window position
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_v.png")
        pixmap = QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        
        # Create close button
        self.close_button = QtWidgets.QPushButton("EXIT", self)
        self.close_button.setStyleSheet("""
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
        self.close_button.clicked.connect(self.close)
        #--------------------------------
        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(int(config.scale*50), int(config.scale*75),
                                       int(config.scale*50), int(config.scale*75)) # L, Up, R, Down
        self.setLayout(main_layout)
        #--------------------------------

        # Buttons and widgets
        self.txt_file = config.txt_file
        B1 = os.path.join(config.destination, "Button1.png")
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        self.V_check = os.path.join(config.destination, "Vibe_check.png")
        self.V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
        #--------------------------------

        # Text-To-Speech button
        self.tts_button = QtWidgets.QPushButton("READ")
        self.tts_button.setMinimumSize(128, 64)
        self.tts_button.setMaximumSize(128, 64)
        self.tts_button.setStyleSheet(f"""
            QPushButton {{
                color: hotpink;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border: 2px solid hotpink;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B1}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
                color: black;
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
                color: black;
            }}
        """)
        self.tts_button.clicked.connect(self.read_text)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(25)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        self.tts_button.setGraphicsEffect(glow_effect)
        main_layout.addWidget(self.tts_button, alignment=Qt.AlignCenter)
        #--------------------------------

        # Text field
        self.text_field = QtWidgets.QTextEdit(self)
        self.text_field.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        self.text_field.setMinimumSize(int(config.scale*128), int(config.scale*128))
        self.text_field.setMaximumSize(int(config.scale*256), int(config.scale*256))
        main_layout.addWidget(self.text_field)
        #--------------------------------

        # Run a timed glitch over the text
        self.setup_glitch_timer(self.text_field, 
                                interval=1500, 
                                glitch_duration=500)
        #--------------------------------

        # Ensure the app works as intended
        self.adjust_close_button_position()
        self.close_button.raise_()
    #--------------------------------

    # Functions
    #--------------------------------
    def adjust_close_button_position(self):
        """
        re-position close button to top-right corner
        before raising (based on window size)
        """
        self.close_button.setGeometry(self.width() - int(config.scale*60), int(config.scale*30),
                                      int(config.scale*50), int(config.scale*30)) # L, H, R, W
    #--------------------------------
    def setup_glitch_timer(self, widget, interval=2000, glitch_duration=300):
        """
        bind glitch to a widget
        """
        print("setting up glitches")
        self.glitch_timer = QTimer()
        self.glitch_timer.timeout.connect(lambda: self.apply_fragment_effect(widget,
                                                                 duration=glitch_duration))
        self.glitch_timer.start(interval)
    # sub-function ^
    def apply_fragment_effect(self, widget, duration=300, colors=None):
        print("glitches running")
        if colors is None: # randomize colours
            colors = [QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))]

        painter = QPainter(widget)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        painter.setPen(pen)

        for _ in range(10):
            x_start = random.randint(0, widget.width())
            y_start = random.randint(0, widget.height())
            x_end = x_start + random.randint(-20, 20)
            y_end = y_start + random.randint(-20, 20)
            painter.drawLine(x_start, y_start, x_end, y_end)
        painter.end()
    #--------------------------------
    def read_text(self):
        """
        does what the button says
        """
        text = "Hello there."
        engine = pyttsx3.init()
        engine.setProperty('rate', 125) # base is 150
        """voices = engine.getProperty('voices')
        for voice in voices:
            print(voice, voice.id)
            engine.setProperty('voice', voice.id)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        use on windows 11"""
        engine.say(text)
        engine.runAndWait()
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TtS()
    window.show()
    app.exec_()
