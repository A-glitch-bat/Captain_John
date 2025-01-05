#--------------------------------

# Imports
import speech_recognition as sr
from PyQt5.QtCore import QObject, pyqtSignal
#--------------------------------

# Speech head class
class SpeechHead(QObject):
    # ready to send response signal to main thread
    text_detected = pyqtSignal(str)

    def __init__(self):
        super(SpeechHead, self).__init__()
        self.voice_recognizer = sr.Recognizer()
        self.running = True

    def listen(self):
        try:
            with sr.Microphone() as source:
                self.voice_recognizer.adjust_for_ambient_noise(source)
                while self.running:
                    try:
                        audio = self.voice_recognizer.listen(source, timeout=0.5, phrase_time_limit=5)
                        if not self.running:
                            break
                        text = self.voice_recognizer.recognize_google(audio)
                        
                        print(f"Detected speech: {text}")
                        self.text_detected.emit(text) # signal to main thread
                    except sr.WaitTimeoutError:
                        # continue listening if not shut down
                        continue
                    except sr.UnknownValueError:
                        print("Speech Recognition could not understand the audio.")
                        self.text_detected.emit("I didn't quite catch that.")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google API: {e}")
                        self.text_detected.emit(f"API error: {str(e)}")
        except Exception as e:
            print(f"Got exception error: {e}")
            self.text_detected.emit(f"Exception error: {str(e)}")

    def stop(self):
        self.running = False
#--------------------------------
