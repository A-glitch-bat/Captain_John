#--------------------------------

# Imports
import os
import threading
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QPixmap, QMovie
from PyQt5.QtCore import Qt, QSize

from AI_heads.ASR_head import ASRHead
from audio.audioplayer import AmbientPlayer
from tasks.spotifyauth import SpotifyAPI
from elements.glitchwidget import GlitchWidget
from elements.status_button import StatusButton
import config
#--------------------------------

# List interaction class
class Speechbot(QtWidgets.QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        #--------------------------------
        self.main_window = main_window

        # Set up main window properties
        self.setWindowTitle("Speech interface")
        self.setWindowFlags(Qt.FramelessWindowHint) # remove window border
        self.setAttribute(Qt.WA_TranslucentBackground) # transparent background
        self.setGeometry(int((config.scale-0.45)*200), int((config.scale-0.40)*150 + int(config.scale*400)), 
                         int(config.scale*350), int(config.scale*450))  # window position, size
        self.speech_listener = ASRHead()
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
        self.B1 = os.path.join(config.destination, "Button1.png")
        self.B1_pressed = os.path.join(config.destination, "Button1_pressed.png")
        self.V_check = os.path.join(config.destination, "icons/confirm.png")
        self.V_cancel = os.path.join(config.destination, "icons/cancel.png")
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
                border: none;
                padding: 12px 24px;
                text-align: center;
                background-image: url('{self.B1}');
            }}
            QPushButton:hover {{
                background-image: url('{self.B1_pressed}');
                color: black;
            }}
            QPushButton:pressed {{
                background-image: url('{self.B1_pressed}');
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
                border: none;
                padding: 12px 24px;
                text-align: center;
                background-image: url('{self.B1}');
            }}
            QPushButton:hover {{
                background-image: url('{self.B1_pressed}');
                color: black;
            }}
            QPushButton:pressed {{
                background-image: url('{self.B1_pressed}');
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
        self.launch_speech()

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
        start listener
        """
        if self.speech_listener.running: self.shutdown_speech()
        else:
            self.speech_listener.text_detected.connect(self.process_detected_command)
            self.listener_thread = threading.Thread(
                target=self.speech_listener.listen,
                daemon=True # terminate thread on main app close
            )
            self.listener_thread.start()
            self.tts_onoff.set_status(1)
            self.text_field.append("Speech head ready")

    # sub-function ^
    def process_detected_command(self, detected_speech):
        print(f"""Processing: {detected_speech}""")

        if "stop" in detected_speech or "shut down" in detected_speech or "error" in detected_speech:
            #self.shutdown_speech()
            print("shut down")
        elif "play" in detected_speech or "music" in detected_speech:
            #self.spotify_start()
            print("spotify")
        elif "timer" in detected_speech or "countdown" in detected_speech:
            #self.start_timer(480)
            print("timer")

    # sub-function ^
    def shutdown_speech(self):
        """
        shut down the speech listener and TTS
        """
        self.speech_listener.stop()
        self.listener_thread.join()
        self.tts_onoff.set_status(None)
        self.text_field.append("Speech head stopped")
    #--------------------------------
    def bot_route(self):
        """
        bot route based on radio main
        """
        if self.main_window.radio_one.isChecked():
            return "mainbot"
        elif self.main_window.radio_two.isChecked():
            return "schizobot"
        else: return "routerbot"
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
    def spotify_start(self, keywords=None):
        """
        main spotify handling function
        """
        if keywords:
            self.spotify_API.play_track(keywords)
        else:
            self.spotify_API.playlist()
    #--------------------------------
    def start_timer(self, seconds):
        """
        start timer
        """
        stopwatch_script = os.path.join(os.path.dirname(__file__), "tasks/timer.py")
        subprocess.Popen(
            ["start", "cmd", "/c", f"python {stopwatch_script} {seconds}"],
            shell=True,
        )
    #--------------------------------
    def closeEvent(self, event):
        self.shutdown_speech()
        super().closeEvent(event)
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Speechbot()
    window.show()
    app.exec_()
