from PyQt5 import QtWidgets

class SimpleInputOutputApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Input and Output")
        self.setGeometry(100, 100, 400, 300)
        layout = QtWidgets.QVBoxLayout()

        # input
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("Type your input here")
        layout.addWidget(self.input_field)
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.display_output)
        layout.addWidget(self.submit_button)

        # output
        self.output_display = QtWidgets.QTextEdit(self)
        self.output_display.setReadOnly(True)  # Make the output area read-only
        layout.addWidget(self.output_display)

        self.setLayout(layout)

    def display_output(self):
        # simple return
        input_text = self.input_field.text()
        if input_text:
            self.output_display.append(f"> {input_text}")
            self.input_field.clear()

# testing - run app
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SimpleInputOutputApp()
    window.show()
    app.exec_()
