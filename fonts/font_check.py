from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
import sys

# Empty QApplication to initialise fonts
app = QApplication(sys.argv)

# Get font list
font_database = QFontDatabase()
available_fonts = font_database.families()

# Font names to external file
with open("font.txt", "w") as file:
    file.write("Available fonts:\n")
    for font in available_fonts:
        file.write(font + "\n")

app.exit()
