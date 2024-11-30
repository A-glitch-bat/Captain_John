#--------------------------------

# Imports
import sys
import subprocess
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import config
from panel import InfoPanel
from aihead import AIhead
from ttshead import TtS
#--------------------------------

# Main class
class CustomWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up the main window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # transparent background
        self.setGeometry(int((config.scale-0.45)*200), int((config.scale-0.40)*150), 
                         int(config.scale*550), int(config.scale*400))  # window size, window position
        #--------------------------------

        # Load and set the background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_h.png")
        pixmap = QtGui.QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        
        # Create custom close button
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
        
        # Create the central widget and horizontal layout for buttons and list
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(int(config.scale*75), int(config.scale*75),
                                       int(config.scale*75), int(config.scale*75)) # L, Up, R, Down
        central_widget.setLayout(main_layout)

        # Create a vertical layout for buttons on the left
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QVBoxLayout()
        button_container.setLayout(button_layout)
        button_container.setMinimumWidth(int(config.scale * 150))
        main_layout.addWidget(button_container, alignment=QtCore.Qt.AlignLeft)

        #--------------------------------
        # Buttons and widgets
        self.txt_file = config.txt_file
        B1 = os.path.join(config.destination, "Button1.png")
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        self.V_check = os.path.join(config.destination, "Vibe_check.png")
        self.V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
        #--------------------------------
        # VS Code Button
        open_vscode_button = QtWidgets.QPushButton("CODE")
        open_vscode_button.setMinimumSize(128, 64)
        open_vscode_button.setMaximumSize(128, 64)
        open_vscode_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        open_vscode_button.clicked.connect(self.open_vscode)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QtGui.QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        open_vscode_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(open_vscode_button)
        #--------------------------------
        # Info Butoon
        self.info_button = QtWidgets.QPushButton("INFO", self)
        self.info_button.setMinimumSize(128, 64)
        self.info_button.setMaximumSize(128, 64)
        self.info_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        self.info_button.clicked.connect(self.open_info_panel)
        
        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QtGui.QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        self.info_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(self.info_button)
        #--------------------------------
        # AI start button
        AI_button = QtWidgets.QPushButton("CHAT", self)
        AI_button.setMinimumSize(128, 64)
        AI_button.setMaximumSize(128, 64)
        AI_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        AI_button.clicked.connect(self.start_AI)

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QtGui.QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        AI_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(AI_button)
        #--------------------------------
        # Listmaker button
        list_button = QtWidgets.QPushButton("TEST", self)
        list_button.setMinimumSize(128, 64)
        list_button.setMaximumSize(128, 64)
        list_button.setStyleSheet(f"""
            QPushButton {{
                color: black;
                font-weight: bold;
                font-size: 15px;
                font-family: OCR A Extended;
                border-radius: 10px;
                padding: 12px 24px;
                text-align: left;
                background-image: url('{B2}');
            }}
            QPushButton:hover {{
                background-image: url('{B2_pressed}');
            }}
            QPushButton:pressed {{
                background-image: url('{B2_pressed}');
            }}
        """)
        list_button.clicked.connect(self.start_ttshead)
        self.start_ttshead() # auto-start for convenience

        glow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QtGui.QColor("hotpink"))
        glow_effect.setOffset(0, 0)

        list_button.setGraphicsEffect(glow_effect)
        button_layout.addWidget(list_button)
        #--------------------------------
        # Stretchable space to push buttons to the top
        button_layout.addStretch()
        #--------------------------------

        # Create a vertical layout for the list on the right
        list_layout = QtWidgets.QVBoxLayout()
        input_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(list_layout)
        list_layout.addLayout(input_layout)

        # Terminal display
        self.terminal_display = QtWidgets.QListWidget(self)
        self.terminal_display.setStyleSheet("""
            QListWidget {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        self.terminal_display.setMinimumSize(int(config.scale*128), int(config.scale*128))
        self.terminal_display.setMaximumSize(int(config.scale*256), int(config.scale*256))
        list_layout.addWidget(self.terminal_display)

        # Input
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("add to list...")
        self.input_field.returnPressed.connect(self.write_input)
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
        self.submit_button.setIcon(QtGui.QIcon.fromTheme(self.V_check))
        self.submit_button.setFixedSize(30, 30)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 2px solid hotpink;
            }
        """)
        self.submit_button.clicked.connect(self.write_input)        
        input_layout.addWidget(self.submit_button)
        #--------------------------------
        # Ensure the app works as intended
        self.read_list()
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
    def open_vscode(self):
        folder_path = "C:/John"
        subprocess.Popen(["code", folder_path], shell=True)
    #--------------------------------
    def open_info_panel(self):
        """
        Open InfoPanel on button click
        """
        self.info_panel = InfoPanel() # prevent garbage-collection
        self.info_panel.show()
    #--------------------------------
    def start_AI(self):
        """
        Open AI head on button click
        """
        self.aihead = AIhead() # prevent garbage-collection
        self.aihead.show()
    #--------------------------------
    def start_ttshead(self):
        """
        Open list display on button click
        """
        self.listdisplay = TtS() # prevent garbage-collection
        self.listdisplay.show()
    #--------------------------------
    def write_input(self):
        """
        write text to file
        """
        input_text = self.input_field.text()
        if input_text: # input exists
            self.append_text(self.txt_file, input_text)
            self.input_field.clear() #clear
            self.read_list()
    # sub-function ^
    def append_text(self, file_path, text):
        """
        open file, append text, close file
        """
        with open(file_path, "a+") as file:
            file.seek(0, 2) # pointer to the end of the file
            if file.tell() > 0:
                file.seek(file.tell() - 1) # find last character
                last_char = file.read(1)
                if last_char != "\n": # confirm new line
                    file.write("\n")
            file.write(text)
    # sub-function ^
    def delete_item(self, item, checkbox):
        """
        delete the line from the text file and remove 
        the list item if the checkbox is checked
        """
        #print(checkbox)
        if checkbox == 1:
            # delete line if checkbox is ticked
            with open(self.txt_file, "r") as file:
                lines = file.readlines()
            with open(self.txt_file, "w") as file:
                for line in lines:
                    if line.strip() != item.text():
                        file.write(line)

            # also remove from the list widget
            row = self.terminal_display.row(item)
            self.terminal_display.takeItem(row)
    #--------------------------------
    def read_list(self):
        """
        text file display
        """
        try:
            with open(self.txt_file, "r") as file:
                lines = file.readlines()
            self.terminal_display.clear()
            for line in lines:
                line = line.strip()
                self.add_list_item(line)
        except FileNotFoundError:
            self.terminal_display.clear()
            self.terminal_display.addItem("Error: 'list.txt' not found.")
    # sub-function ^
    def add_list_item(self, text):
        """
        add a line of text to the list widget
        """
        row_widget = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setContentsMargins(2, 2, 2, 2)
        row_layout.setSpacing(5)

        # create checkbox, text label and delete button
        checkbox = QtWidgets.QCheckBox()
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: hotpink;
            }
        """)
        text_label = QtWidgets.QLabel(text)
        text_label.setStyleSheet("color: hotpink; font-size: 14px; font-family: OCR A Extended;")

        delete_button = QtWidgets.QPushButton()
        delete_button.setIcon(QtGui.QIcon(self.V_cancel))
        delete_button.setIconSize(QtCore.QSize(24, 24))
        delete_button.setFixedSize(30, 30)
        delete_button.setStyleSheet("border: none;")

        # checkbox -> text -> delete button
        row_layout.addWidget(checkbox)
        row_layout.addWidget(text_label)
        row_layout.addWidget(delete_button)

        row_layout.setAlignment(QtCore.Qt.AlignLeft)
        row_widget.setLayout(row_layout)
        list_item = QtWidgets.QListWidgetItem(self.terminal_display)
        list_item.setSizeHint(row_widget.sizeHint())  # Match size to contents
        self.terminal_display.setItemWidget(list_item, row_widget)

        # delete button click connection
        delete_button.clicked.connect(lambda: self.delete_item(list_item, checkbox.isChecked()))
    # sub-function ^
    def handle_checkbox_toggled(self, state, text):
        """
        checkbox toggling
        """
        for i in range(self.terminal_display.count()):
            item = self.terminal_display.item(i)
            if item.text() == text:
                if state == QtCore.Qt.Checked:
                    font = item.font()
                    font.setStrikeOut(True)
                    item.setFont(font)
                    item.setForeground(QtCore.Qt.darkGray)
                else:
                    # restore default item look
                    font = item.font()
                    font.setStrikeOut(False)
                    item.setFont(font)
                    item.setForeground(QtGui.QBrush(QtGui.QColor("hotpink")))
    #--------------------------------

#--------------------------------
# Wake John up
app = QtWidgets.QApplication(sys.argv)
window = CustomWindow()
window.show()
sys.exit(app.exec_())
#--------------------------------
