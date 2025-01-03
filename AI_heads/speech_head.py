#--------------------------------

# Imports
import speech_recognition as sr
from PyQt5.QtCore import QObject, pyqtSignal
"""
pip install SpeechRecognition
pip install PyAudio
pip install pygame
# List all microphones
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
"""
#--------------------------------

# Speech head class
class SpeechHead(QObject):
    # ready to send response signal to main thread
    text_detected = pyqtSignal(str)

    def __init__(self):
        super(SpeechHead, self).__init__()
        self.voice_recognizer = sr.Recognizer()
        self.device_index = 1
        self.running = True

    def listen(self):
        while self.running:
            try:
                with sr.Microphone(device_index=self.device_index) as source:
                    self.voice_recognizer.adjust_for_ambient_noise(source)
                    audio = self.voice_recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.voice_recognizer.recognize_google(audio)
                    #print(f"Detected speech: {text}")
                    self.text_detected.emit(text) # signal to main thread
            except sr.UnknownValueError:
                self.text_detected.emit("I didn't quite catch that.")
            except sr.RequestError as e:
                self.text_detected.emit(f"API error: {str(e)}")
            except Exception as e:
                self.text_detected.emit(f"Exception error: {str(e)}")

    def stop(self):
        self.running = False
#--------------------------------
