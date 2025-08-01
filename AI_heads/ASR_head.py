#--------------------------------

# Imports
import os
import json
import queue
import numpy as np
import scipy.signal
import requests

import vosk
import pygame
import sounddevice as sd
import speech_recognition as sr
import whisper
from PyQt5.QtCore import QObject, pyqtSignal

from AI_heads.TTS_head import TTSHead
import config
#--------------------------------

# Speech head class
class ASRHead(QObject):
    text_detected = pyqtSignal(str)

    def __init__(self):
        super(ASRHead, self).__init__()
        #--------------------------------

        wl_path = os.path.join(config.base_folder,"models/vosk-model-small-en-us-0.15")
        self.wakeword_listener = None
        try:
            self.wakeword_listener = vosk.Model(wl_path)
        except Exception as e:
            print(f"Error loading Vosk model: {e}")

        self.speech_engine = TTSHead()
        self.running = False
        self.q = queue.Queue()
        self.audio_path = os.path.join(config.base_folder, "audio/success.mp3")
        self.recognizer = sr.Recognizer()
        self.transcriber = whisper.load_model("small")
        pygame.mixer.init()

    def listen(self):
        print("Listening for wake word...")
        self.running = True
        self.loop = False
        pygame.mixer.Sound(self.audio_path).set_volume(0.5)
        sound = pygame.mixer.Sound(self.audio_path)
        
        if self.wakeword_listener is None:
            print("Error: Listener not loaded")
            self.stop()

        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.q.put(bytes(indata))

        with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                               channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(self.wakeword_listener, 16000)

            while self.running:
                try:
                    data = self.q.get(timeout=1.0)
                except queue.Empty:
                    continue

                text = ""
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").lower()
                    print("Text = "+text)
                with self.q.mutex:
                    self.q.queue.clear()

                if "john" in text or "captain" in text:
                    print("John listening.")
                    sound.play()

                    self.loop = True
                    while self.loop:
                        with sr.Microphone() as source:
                            print("Listening...")
                            audio = self.recognizer.listen(source)
                            print("Recording complete")

                        # Convert to float32 numpy array from raw audio (usually 16-bit signed integers)
                        raw_audio = np.frombuffer(audio.get_raw_data(), np.int16).astype(np.float32) / 32768.0

                        # Resample to 16000 Hz if needed (most mics default to 44.1kHz or 48kHz)
                        original_rate = audio.sample_rate
                        if original_rate != 16000:
                            num_samples = int(len(raw_audio) * 16000 / original_rate)
                            resampled_audio = scipy.signal.resample(raw_audio, num_samples)
                        else:
                            resampled_audio = raw_audio

                        # Transcribe directly from numpy array
                        result = self.transcriber.transcribe(resampled_audio, language="en")
                        msg = result["text"]
                        DATA = {'message':msg}

                        route_task = requests.post(url = os.path.join(config.URL, "routerbot"),
                                                data=DATA).text
                        
                        if self.speech_engine.free:
                            print("Reading task route")
                            self.speech_engine.speak(route_task)

                        # Exit if requested
                        if result=="thank_you" or result=="cancel":
                            self.loop = False

                        self.text_detected.emit(route_task, msg)
    #--------------------------------

    def stop(self):
        print("Stopping listener...")
        self.running = False
        self.q.put(b'')
#--------------------------------
