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
        self.engine.setProperty('rate', 140)

        # Adjust properties
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        #--------------------------------

    # Functions
    def speak(self, text):
        """
        read the text
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def shutdown(self):
        """
        shut down tts engine
        """
        self.engine.stop()
    #--------------------------------

# Temporary main
if __name__ == "__main__":
    tts = TTSHead()
    tts.speak("Testing all voice options")
