#--------------------------------

# Imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
#--------------------------------

# Spotify API
class SpotifyAPI():
    def __init__(self):
        super(SpotifyAPI, self).__init__()

        # Spotify authentication
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=config.spotify_client_id,
            client_secret=config.spotify_client_secret,
            redirect_uri="http://localhost:5000",
            scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        ))
        # select first computer with active spotify
        devices = self.sp.devices()
        computer_device = next((d for d in devices["devices"] if d["type"] == "Computer"), {"id": None})
        self.device_ID = computer_device["id"]
    #--------------------------------
    # Functions

    def get_current_song(self):
        """
        get stats
        """
        current_track = self.sp.current_playback()
        if current_track:
            print(f"Now playing: {current_track['item']['name']} by {current_track['item']['artists'][0]['name']}")
        else:
            print("No song is currently playing.")
    #--------------------------------

    def play_track(self, keywords):
        """
        play track from keywords
        """
        results = self.sp.search(q=keywords, type="track", limit=1)
        
        # double check for a valid device
        if not self.device_ID:
            devices = self.sp.devices()
            computer_device = next((d for d in devices["devices"] if d["type"] == "Computer"), {"id": None})
            self.device_ID = computer_device["id"]
            if not self.device_ID:
                print("No device found.")

        # get URI and play
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            self.sp.start_playback(device_id=self.device_ID, uris=[track_uri])
            print(f"Playing: {results['tracks']['items'][0]['name']}")
        else:
            print("No track found.")
#--------------------------------