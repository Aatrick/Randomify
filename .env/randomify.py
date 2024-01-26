import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import webbrowser
import pandas as pd
import random 
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

username = 'Emilio'
clientID = ''
clientSecret = ''
redirectURI = 'http://google.com/' 

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirectURI)
try:
    token_dict = oauth_object.get_cached_token()
except spotipy.oauth2.MaxRetries:
    print("Max Retries reached")
    # Handle the MaxRetries exception here
except spotipy.oauth2.ResponseError as e:
    if e.status == 429:
        print("Too many 429 error responses")
        # Handle the ResponseError exception here
    else:
        raise e
#token_dict = oauth_object.get_access_token() 
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_tracks(playlist_id):
    playlist = sp.playlist_tracks(playlist_id)["items"]

    track_list = []
    offset = 0
    while True:
        playlist = sp.playlist_tracks(playlist_id, offset=offset)["items"]
        if not playlist:
            break
        offset += 100
        for track in playlist:
            track_id = track["track"]["id"]
            track_name = track["track"]["name"]
            track_artist = track["track"]["artists"][0]["name"]
            track_duration = int(track["track"]["duration_ms"] / 1000)
            track_tuple = (track_id, track_name, track_artist, track_duration)
            track_list.append(track_tuple)
    
    return track_list

playlist_songs=get_tracks("19807JSM82MpH1Krr2pO7I")

while True:
    track = random.choice(playlist_songs)
    track_id = track[0]
    track_name = track[1]
    track_artist = track[2]
    track_duration = track[3]
    song = f"https://open.spotify.com/track/{track_id}"
    webbrowser.open(song)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    print(f"Now playing: {track_name} \nfrom {track_artist}\n")
    time.sleep(track_duration)
