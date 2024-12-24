#--------------------------------

# Imports
import sys
import subprocess
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from transformers import AutoModelForCausalLM, AutoTokenizer
from johnsAI import JohnsNN
import config
#--------------------------------

# AI head class
class AIhead(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up the main window properties
        self.setWindowTitle("Base for AI component")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # transparent background
        self.setGeometry(int((config.scale-0.45)*200) + int(config.scale*350), int((config.scale-0.40)*150 + int(config.scale*400)), 
                         int(config.scale*350), int(config.scale*450))  # window size, window position
        
        self.tokenizer = None
        self.model = None
        self.chat_history_ids = None
        #--------------------------------

        # Load and set the custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_v.png")
        pixmap = QtGui.QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
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
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        V_check = os.path.join(config.destination, "Vibe_check.png")
        V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
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
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.setIcon(QtGui.QIcon.fromTheme(V_check))
        self.submit_button.setFixedSize(30, 30)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 2px solid hotpink;
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
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        
        main_layout.addWidget(self.output_display)
        self.output_display.append(f"Hello! How may I help you? \n")

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
    def launch_AI(self):
        """
        load model and tokenizer when needed
        """
        model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
    #--------------------------------
    def get_reply(self):
        user_input = self.input_field.text()
        if user_input == "":
            return
        elif self.model == None:
            self.launch_AI()

        # Ensure the tokenizer has a padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Tokenize input and get reply from model
        inputs = self.tokenizer(user_input, return_tensors="pt",
                                padding=True, truncation=True)
        outputs = self.model.generate(
            **inputs,
            pad_token_id=self.tokenizer.eos_token_id,
            num_beams=2,
            max_length=75,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_p=0.9,
            temperature=0.8,
            early_stopping=True
        )
        reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Display the conversation
        self.output_display.append(f"Q: {user_input}\n")
        if reply.startswith(user_input):
            reply = reply[len(user_input):].strip()
        self.output_display.append(f"B: {reply}")

        self.output_display.append(f"---------------------- \n")
        self.input_field.clear()
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AIhead()
    window.show()
    app.exec_()
