from PyQt5 import QtWidgets, QtGui, QtCore
import os
import torch
import config
#--------------------------------

# List interaction class
class ListMaker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #--------------------------------

        # Set up main window properties
        self.setWindowTitle("Base for list component")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # remove window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # transparent background
        self.setGeometry(int(config.scale*200)+int(config.scale*350), int(config.scale*550), 
                         int(config.scale*350), int(config.scale*450))  # window size, window position
        #--------------------------------

        # Load custom background image
        self.background_label = QtWidgets.QLabel(self)
        border_location = os.path.join(config.destination, "xmas_visuals/xmas_border_v.png")
        pixmap = QtGui.QPixmap(border_location)
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
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
        # Buttons and widgets
        self.txt_file = config.txt_file
        B2 = os.path.join(config.destination, "Button2.png")
        B2_pressed = os.path.join(config.destination, "Button2_pressed.png")
        self.V_check = os.path.join(config.destination, "Vibe_check.png")
        self.V_cancel = os.path.join(config.destination, "Vibe_cancel.png")
        #--------------------------------

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(int(config.scale*50), int(config.scale*75),
                                       int(config.scale*50), int(config.scale*75)) # L, Up, R, Down
        input_layout = QtWidgets.QHBoxLayout()

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
        main_layout.addLayout(input_layout)

        # Output
        self.output_display = QtWidgets.QListWidget(self)
        self.output_display.setStyleSheet("""
            QListWidget {
                background-color: black;
                color: hotpink;
                font-family: OCR A Extended;
                font-size: 14px;
                border: 2px solid hotpink;
            }
        """)
        
        main_layout.addWidget(self.output_display)
        self.setLayout(main_layout)
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
            row = self.output_display.row(item)
            self.output_display.takeItem(row)
    #--------------------------------
    def read_list(self):
        """
        text file display
        """
        try:
            with open(self.txt_file, "r") as file:
                lines = file.readlines()
            self.output_display.clear()
            for line in lines:
                line = line.strip()
                self.add_list_item(line)
        except FileNotFoundError:
            self.output_display.clear()
            self.output_display.addItem("Error: 'list.txt' not found.")
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
        list_item = QtWidgets.QListWidgetItem(self.output_display)
        list_item.setSizeHint(row_widget.sizeHint())  # Match size to contents
        self.output_display.setItemWidget(list_item, row_widget)

        # delete button click connection
        delete_button.clicked.connect(lambda: self.delete_item(list_item, checkbox.isChecked()))
    # sub-function ^
    def handle_checkbox_toggled(self, state, text):
        """
        checkbox toggling
        """
        for i in range(self.output_display.count()):
            item = self.output_display.item(i)
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

# Temporary main
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ListMaker()
    window.show()
    app.exec_()
