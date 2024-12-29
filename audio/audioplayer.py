#--------------------------------

# Imports
import os
import pygame
import time
import random
import threading
import config
#--------------------------------

# Ambient audio player class
class AmbientPlayer:
    def __init__(self, min_interval=15, max_interval=30):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.is_running = False
        pygame.mixer.init()
    #--------------------------------

    # Functions
    #--------------------------------
    def start(self):
        """
        start and stop ambient audio
        """
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.loop_sound, daemon=True)
            self.thread.start()
            print("Playing ambient sounds")
    # sub-function ^
    def stop(self):
        self.is_running = False
        print("Stopping ambient sounds")
    #--------------------------------
    def loop_sound(self):
        """
        play random ambient sound in random intervals
        """
        while self.is_running:
            rand_audio = random.choice(os.listdir(os.path.join(config.base_folder, "audio/ambient")))
            audio_path = os.path.join(config.base_folder, "audio/ambient/"+rand_audio)
            pygame.mixer.Sound(audio_path).set_volume(0.25)
            sound = pygame.mixer.Sound(audio_path)
            sound.play()

            interval = random.randint(self.min_interval, self.max_interval)
            print(f"Next sound in {interval} seconds...")
            time.sleep(interval)
            if not self.is_running:  # Exit the thread if the flag is False
                break
    #--------------------------------
