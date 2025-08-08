#--------------------------------

# Imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
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
        self.sp = None
        self.device_ID = None
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=config.spotify_client_id,
                client_secret=config.spotify_client_secret,
                redirect_uri="http://127.0.0.1:5000", # local uri
                # allow playback control
                scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing",
                # bypass on fail
                open_browser=False, 
                show_dialog=False
            ))
    
            # select first computer with active spotify
            devices = self.sp.devices()
            computer_device = next((d for d in devices["devices"] if d["type"] == "Computer"), {"id": None})
            self.device_ID = computer_device["id"]
        except Exception as e:
            print(f"Spotify setup failed: {e}")
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

    def playlist(self):
        """
        play basic playlist
        """        
        # double check for a valid device
        if not self.device_ID:
            devices = self.sp.devices()
            computer_device = next((d for d in devices["devices"] if d["type"] == "Computer"), {"id": None})
            self.device_ID = computer_device["id"]
            if not self.device_ID:
                print("No device found.")

        # play the playlist
        playlist_uri = "spotify:playlist:1DrEOtANKVDajkgkuABPAM?si=b2b65d58907247a2"

        self.sp.start_playback(device_id=self.device_ID, context_uri=playlist_uri)
        print("Playing your default playlist!")
#--------------------------------