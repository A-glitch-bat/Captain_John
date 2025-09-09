#--------------------------------

# Imports
import os
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter
from tasks.request_worker import RequestsThread
from AI_heads.summarizer import text_sum
from tasks.scrape import ask_the_web
import config
#--------------------------------

# Chatbot class
class Chatbot(QtWidgets.QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        #--------------------------------
        self.main_window = main_window
        self.f_path = os.path.dirname(os.path.abspath(__file__))
        self.disect = False

        # Set up main window properties
        self.setWindowTitle("Chat interface")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # transparent background
        self.setGeometry(int((config.scale-0.45)*200) + int(config.scale*350), int((config.scale-0.40)*150 + int(config.scale*400)), 
                         int(config.scale*350), int(config.scale*450))  # window position, size
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        background_top_path = os.path.join(self.f_path, "visuals/V_background2.png")
        background_bottom_path = os.path.join(self.f_path, "visuals/V2_bb.png")
        top_pixmap = QPixmap(background_top_path).scaled(
            self.width(), self.height(), 
            Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        bottom_pixmap = QPixmap(background_bottom_path).scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        composed_image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        composed_image.fill(Qt.transparent)

        # Overlay backgrounds
        painter = QPainter(composed_image)
        painter.setOpacity(config.transbckg)
        painter.drawPixmap(0, 0, bottom_pixmap)
        painter.setOpacity(1.0)
        painter.drawPixmap(0, 0, top_pixmap)
        painter.end()

        # Convert back to QPixmap and apply to label
        pixmap = QPixmap.fromImage(composed_image)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Create the custom "X" close button
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
        # Buttons and emblems
        self.B2 = os.path.join(self.f_path, "visuals/Button2.png")
        self.B2_pressed = os.path.join(self.f_path, "visuals/Button2_pressed.png")
        self.V_check = os.path.join(self.f_path, "visuals/icons/confirm.png")
        self.V_cancel = os.path.join(self.f_path, "visuals/icons/cancel.png")
        #--------------------------------

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(int(config.scale*50), int(config.scale*75),
                                       int(config.scale*50), int(config.scale*75)) # L, Up, R, Down
        input_layout = QtWidgets.QHBoxLayout()

        # Input
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("request...")
        self.input_field.returnPressed.connect(self.get_reply)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 125);
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
                border-radius: 7px;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.setIcon(QtGui.QIcon.fromTheme(self.V_check))
        self.submit_button.setFixedSize(30, 30)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid hotpink;
                border-radius: 7px;
            }
        """)
        self.submit_button.clicked.connect(self.get_reply)
        
        input_layout.addWidget(self.submit_button)
        main_layout.addLayout(input_layout)

        # Output
        self.output_display = QtWidgets.QTextEdit(self)
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 125);
                color: hotpink;
                font-family: 'OCR A Extended';
                font-size: 14px;
                border: 2px solid hotpink;
                border-radius: 14px;
                padding: 6px;
            }
        """)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(50)
        effect.setColor(QtGui.QColor(255, 0, 255, 75))
        effect.setOffset(0, 0)
        self.output_display.setGraphicsEffect(effect)

        main_layout.addWidget(self.output_display)
        self.output_display.append(f"B: Systems online. Standing by.\n")
        self.output_display.append(f"---------------------- \n")

        self.setLayout(main_layout)
        #--------------------------------
        # Ensure the app can be closed
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
    def get_reply(self):
        """
        send request to capnjohn on RPI and display it
        """
        user_input = self.input_field.text()
        if user_input == "":
            return
        self.input_field.clear()
        self.output_display.append(f"Q: {user_input}\n")
        self.output_display.append(f"B: ")

        # Request answer from URL on separate thread
        DATA = {'message':user_input}
        self.reqThread = RequestsThread(DATA, self.bot_route())
        self.reqThread.response.connect(self.replyWaiter)
        self.reqThread.start()

    # sub-function ^
    def replyWaiter(self, reply):
        """
        get the bot reply and type it out
        """
        if reply["success"]:
            self.reply = f"{reply['data']}"
        else:
            self.reply = f"Error: {reply['error']}"

        if self.disect:
            analyse = json.loads(reply['data'])
            #--------------------------------
            # 0 -> task not defined yet
            # 1 -> task finished
            # 2 -> short reply, process accordingly
            # 3 -> timer
            # 4 -> music
            # 5 -> idk google it
            #--------------------------------
            if analyse["taskID"] == 1:
                print("task finished") 
            elif analyse["taskID"] == 2:
                print("yesno")
                t, q = analyse["answer"].split(str(analyse["taskID"]), 1)
                print(t);print(q)
            elif analyse["taskID"] == 3:
                print("timer")
            elif analyse["taskID"] == 4:
                print("spotify")
                t, q = analyse["answer"].split(str(analyse["taskID"]), 1)
                print(t);print(q)
            else:
                # Don't know the specific task? Google it!
                print("Googlin' it")
                web_finds = ask_the_web(analyse["answer"])
                print(web_finds)
                combined_snippets = " ".join(web_finds[1].split(". ")[:5])
                self.reply = text_sum(combined_snippets)

        # Type the message
        self.current_index = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.typewriter)
        self.timer.start(25)

    # sub-function ^
    def typewriter(self):
        """
        type the text into the output display, typewriter style
        """
        if self.current_index < len(self.reply):
            char = self.reply[self.current_index]
            self.output_display.insertPlainText(char)
            self.current_index += 1
        else:
            self.output_display.append(f"\n---------------------- \n")
            self.timer.stop()
    #--------------------------------
    def bot_route(self):
        """
        bot route based on radio main
        """
        if self.main_window is not None:
            if self.main_window.radio_one.isChecked():
                self.disect = True
                return "mainbot"
            elif self.main_window.radio_two.isChecked():
                self.disect = False
                return "schizobot"
            self.disect = False
            return "routerbot"
        self.disect = True
        return "mainbot"
#--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Chatbot()
    window.show()
    app.exec_()
