#--------------------------------

# Imports
from PyQt5.QtCore import QObject
import pyttsx3
#--------------------------------

# Text-To-Speech class
class TTSHead(QObject):
    def __init__(self):
        super(TTSHead, self).__init__()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        # Adjust properties
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Try voices[1] for alternative voice

        self.speak("This is a custom voice and speed.")
    #--------------------------------

    # Functions
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
#--------------------------------
