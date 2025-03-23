#--------------------------------

# Imports
import os
import speech_recognition as sr
import pygame
from PyQt5.QtCore import QObject, pyqtSignal
import config
#--------------------------------

# Speech head class
class SpeechHead(QObject):
    # ready to send response signal to main thread
    text_detected = pyqtSignal(str)

    def __init__(self):
        super(SpeechHead, self).__init__()
        self.voice_recognizer = sr.Recognizer()
        self.running = True
        self.audio_path = os.path.join(config.base_folder, "audio/success.mp3")
        pygame.mixer.init()

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
                        #print(f"Detected speech: {text}")

                        if "John" in text:
                            pygame.mixer.Sound(self.audio_path).set_volume(0.5)
                            sound = pygame.mixer.Sound(self.audio_path)
                            sound.play()

                            command = self.voice_recognizer.listen(source, timeout=5, phrase_time_limit=15)
                            send = self.voice_recognizer.recognize_google(command)
                            print(f"Command: {send}")
                            self.text_detected.emit(send) # signal to main thread

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
