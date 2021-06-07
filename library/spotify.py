import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

with open("settings.json") as settings_file:
    main_settings = json.load(settings_file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=main_settings['client_id'],client_secret=main_settings['client_secret'],redirect_uri=main_settings['redirect_uri'],scope="user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state"))

def get_track():
    track = sp.current_user_playing_track()['item']['name']
    return(track)

def play_track(song):
    result = sp.search(song)
    #for k in result['tracks']:
        #print(k)
    result = result['tracks']['items'][0]
    spotify_uri = result['uri']
    sp.start_playback(uris=[spotify_uri])
    return(result)
def pause_music():
    sp.pause_playback()
    return ""
def resume_music():
    sp.start_playback()
    return ""
