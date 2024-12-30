#--------------------------------

# Imports
import os
import pyttsx3
import speech_recognition as sr
import random

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QSize

from glitchwidget import GlitchWidget
from audio.audioplayer import AmbientPlayer
from elements.status_button import StatusButton
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
                         int(config.scale*350), int(config.scale*450))  # window position, size
        self.sound_player = None
        self.tts_engine = None
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "V_background1.png")
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
        self.tts_button = QtWidgets.QPushButton("SPEECH")
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
        self.tts_button.clicked.connect(self.launch_speech)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(25)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        self.tts_button.setGraphicsEffect(glow_effect)
        tts_BoxLayout = QtWidgets.QHBoxLayout()
        tts_BoxLayout.addWidget(self.tts_button)

        self.tts_onoff = StatusButton()
        tts_BoxLayout.addWidget(self.tts_onoff)
        main_layout.addLayout(tts_BoxLayout)
        #--------------------------------

        # Ambient audio button
        self.ambient_button = QtWidgets.QPushButton("AUDIO")
        self.ambient_button.setMinimumSize(128, 64)
        self.ambient_button.setMaximumSize(128, 64)
        self.ambient_button.setStyleSheet(f"""
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
        self.ambient_button.clicked.connect(self.launch_audio)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(25)
        glow_effect.setColor(QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        self.ambient_button.setGraphicsEffect(glow_effect)
        audio_BoxLayout = QtWidgets.QHBoxLayout()
        audio_BoxLayout.addWidget(self.ambient_button)

        self.audio_onoff = StatusButton()
        audio_BoxLayout.addWidget(self.audio_onoff)
        main_layout.addLayout(audio_BoxLayout)
        #--------------------------------

        # Text field
        self.text_field = QtWidgets.QTextEdit(self)
        self.text_field.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0);
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: none;
                padding: 15px;
                margin: 15px;
            }
        """)
        self.text_field.setReadOnly(True)
        self.text_field.setAttribute(Qt.WA_TranslucentBackground, True)
        self.text_field.setMinimumSize(int(config.scale*128), int(config.scale*128))
        self.text_field.setMaximumSize(int(config.scale*256), int(config.scale*256))
        neuromancer_text = (
        "The sky above the port was the color of television, tuned to a dead channel. \n"
        "He jacked out, blinking away the illusion, and stared at the cracked ceiling above him, "
        "wondering how much longer he could keep running."
        )
        self.text_field.setText(neuromancer_text)

        # Stack glitch over text
        glitch_overlay = GlitchWidget(self)
        stacked_layout = QtWidgets.QStackedLayout()
        stacked_layout.addWidget(self.text_field)
        stacked_layout.addWidget(glitch_overlay)
        stacked_layout.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        glitch_container = QtWidgets.QWidget()
        glitch_container.setLayout(stacked_layout)
        main_layout.addWidget(glitch_container)
        def resize_glitch():
            glitch_overlay.setGeometry(self.text_field.geometry())
        glitch_container.resizeEvent = lambda event: resize_glitch()

        # GIF widget
        gif_label = QtWidgets.QLabel(self)
        gif_label.setAlignment(Qt.AlignCenter)
        G1 = os.path.join(config.destination, "square_glitch.gif")
        gif = QMovie(G1)
        gif.setScaledSize(QSize(64, 64))

        gif_label.setMovie(gif)
        gif.start()
        main_layout.addWidget(gif_label)
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
    def launch_audio(self):
        """
        start the sound player
        """
        if not self.sound_player:
            self.sound_player = AmbientPlayer(min_interval=60, max_interval=360)
            self.sound_player.start()
            self.audio_onoff.set_status(self.sound_player)
        else:
            self.sound_player.stop()
            self.sound_player = None
            self.audio_onoff.set_status(self.sound_player)
    #--------------------------------
    def launch_speech(self):
        """
        make the module listen and talk
        """
        if not self.tts_engine:
            self.tts_engine = pyttsx3.init()
            self.tts_onoff.set_status(self.tts_engine)

            text = "Hello there."
            self.tts_engine.setProperty('rate', 125) # base is 150
            """voices = engine.getProperty('voices')
            for voice in voices:
                print(voice, voice.id)
                engine.setProperty('voice', voice.id)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            use on windows 11"""
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

            self.tts_engine = None
            self.tts_onoff.set_status(self.tts_engine)
        else:
            self.tts_engine = None
            self.tts_onoff.set_status(self.tts_engine)
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TtS()
    window.show()
    app.exec_()
