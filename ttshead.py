#--------------------------------

# Imports
import os
import pyttsx3
import speech_recognition as sr
import threading
import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QSize, QThread

from AI_heads.speech_head import SpeechHead
from audio.audioplayer import AmbientPlayer
from tasks.spotifyauth import SpotifyAPI
from elements.glitchwidget import GlitchWidget
from elements.status_button import StatusButton
import config
#--------------------------------

# List interaction class
class TtS(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Speech interface")
        self.setWindowFlags(Qt.FramelessWindowHint) # remove window border
        self.setAttribute(Qt.WA_TranslucentBackground) # transparent background
        self.setGeometry(int((config.scale-0.45)*200), int((config.scale-0.40)*150 + int(config.scale*400)), 
                         int(config.scale*350), int(config.scale*450))  # window position, size
        self.speech_active = None
        self.sound_player = None
        self.speech_listener = None
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 125) # base is 150
        self.spotify_API = SpotifyAPI()
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
        main_layout.setContentsMargins(int(config.scale*25), int(config.scale*75), # L, Up,
                                       int(config.scale*25), int(config.scale*25)) # R, Down
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
        self.text_field.setText("Speech head not active.")

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
    def launch_speech(self):
        """
        make the module listen and talk
        """
        if not self.speech_active:
            # Start up speech head on separate thread
            self.speech_active = 1
            self.tts_onoff.set_status(self.speech_active)

            # Connect signal to slot
            self.speech_listener = SpeechHead()
            self.speech_listener.text_detected.connect(self.process_detected_command)

            self.listener_thread = threading.Thread(target=self.speech_listener.listen)
            self.listener_thread.start()
            self.text_field.append("Speech head ready.")
        else:
            # Shut down speech head and close thread
            self.shutdown_speech()
    # sub-function ^
    def process_detected_command(self, detected_speech):
        if self.speech_active:
            self.text_field.append("Speech head is busy. Please wait...")
            return
        
        response = "I don't know how to answer that."
        if "stop" in detected_speech or "shut down" in detected_speech or "error" in detected_speech:
            self.shutdown_speech()
            response = "Stopping speech module."
        elif "play" in detected_speech or "music" in detected_speech:
            webbrowser.open("https://youtu.be/RRKJiM9Njr8?si=fvPsyxbmB5MjrE_Q")
            response = "Playing MCR."
        
        # Answer last spoken command and set status to stopped
        self.speech_active = 1 # set flag before processing
        self.text_field.append(detected_speech)
        try:
            self.speech_active = 1
            #self.tts_engine.say(response)
            #self.tts_engine.runAndWait()
        finally:
            self.speech_active = None # reset flag
        self.shutdown_speech()
    # sub-function ^
    def shutdown_speech(self):
        """
        shut down the speech listener and TTS
        """
        if self.speech_listener:
            print("Stopping...")
            self.text_field.append("Stopping...")
            self.speech_listener.stop()
            self.listener_thread.join()
        self.speech_listener = None
        self.speech_active = None
        self.tts_onoff.set_status(self.speech_active)
        print("Speech head stopped.")
        self.text_field.append("Speech head stopped.")
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
    def spotify_start(self, keywords):
        """
        main spotify handling function
        """
        self.spotify_API.play_track(keywords)
    #--------------------------------
    def closeEvent(self, event):
        self.shutdown_speech()
        super().closeEvent(event)
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TtS()
    window.show()
    app.exec_()
