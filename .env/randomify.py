import spotipy
import json
import webbrowser
import pandas as pd
import random 

from spotipy.oauth2 import SpotifyClientCredentials

username = 'Emilio'
clientID = 'f956c798c044418b9204fe6fc9d303ed'
clientSecret = '5ca12d350e574940852ab5dde947abdd'
redirectURI = 'http://google.com/' 

oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()


client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


def call_playlist(creator, playlist_id):
    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Initialize offset
    offset = 0

    while True:
        playlist = sp.user_playlist_tracks(creator, playlist_id, offset=offset)["items"]
        if not playlist:
            break

        for track in playlist:
            playlist_features = {}
            playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
            playlist_features["album"] = track["track"]["album"]["name"]
            playlist_features["track_name"] = track["track"]["name"]
            playlist_features["track_id"] = track["track"]["id"]
            
            audio_features = sp.audio_features(playlist_features["track_id"])[0]
            for feature in playlist_features_list[4:]:
                playlist_features[feature] = audio_features[feature]
            
            track_df = pd.DataFrame(playlist_features, index = [0])
            playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
        # Increase the offset by 100 (Spotify's limit per request)
        offset += 100

    return playlist_features['track_id']

playlist_songs = call_playlist("Emilio","19807JSM82MpH1Krr2pO7I")

def randomify():
    for i in range(50):
        random_song = random.choice(playlist_songs)
        spotipy.add_to_queue(random_song)

randomify()

#print(json.dumps(user,sort_keys=True, indent=4))
#while True:
    #print("Welcome, "+ user['display_name'])
    #print("0 - Exit")
    #print("1 - Search for a Playlist")
    #choice = int(input("Your Choice: "))
    #if choice == 1:
    #    # Get the Song Name.
    #    searchQuery = input("Enter Song Name: ")
    #    # Search for the Song.
    #    searchResults = spotifyObject.search(searchQuery,1,0,"track")
    #    # Get required data from JSON response.
    #    tracks_dict = searchResults['tracks']
    #    tracks_items = tracks_dict['items']
    #    song = tracks_items[0]['external_urls']['spotify']
    #    # Open the Song in Web Browser
    #    webbrowser.open(song)
    #    print('Song has opened in your browser.')
    #elif choice == 0:
    #    break
    #else:
    #    print("Enter valid choice.")