import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8080",
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

# Get current playback state
current_track = sp.current_playback()

if current_track:
    print(f"Now playing: {current_track['item']['name']} by {current_track['item']['artists'][0]['name']}")
else:
    print("No song is currently playing.")
