# IMPORTS
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time

# GLOBAL
username = sys.argv[1] # Spotify name in command line after runnong pythong e.g. "python main.py usernameHere"

# FUNCTIONS
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing'

# Erase cache and prompt user permission
try:
    token = util.prompt_for_user_token(username, scope, client_id='YOUR CLIENT ID HERE',
                        client_secret='YOUR CLIENT SECRET HERE',
                        redirect_uri='http://localhost:8888/callback/')
except:
    os.remove(f".cache={username}")
    token = util.prompt_for_user_token(username, scope, client_id='YOUR CLIENT ID HERE',
                        client_secret='YOUR CLIENT SECRET HERE',
                        redirect_uri='http://localhost:8888/callback/')

spotifyObject = spotipy.Spotify(auth=token)


def songChangeCheck(currentTrack, spotifyObject):
    trackProgress = currentTrack["progress_ms"]
    trackID = currentTrack["item"]["id"]
    track_duration = spotifyObject.track(trackID)['duration_ms']

    if (track_duration - trackProgress) < 30000: # change 30 seconds to a percentage of the song
        print("Track passed")
    else:
        print("Track skipped")

        # add data to database
        # ++ to skipped count
        # Database will have 3 collumns
        # {
        #   "track id" : trackID
        #   "skipCount" : skipCount
        #   "reachedThreshhold" : True/False
        # }


def main(spotifyObject):
    currentTrackName = spotifyObject.current_user_playing_track()["item"]["name"]
    currentTrack = spotifyObject.current_user_playing_track()
    CurrentTrackArtist = spotifyObject.current_user_playing_track()["item"]["artists"][0]["name"]

    while True:
        newCurrentTrack = spotifyObject.current_user_playing_track()
        newCurrentTrackArtist = spotifyObject.current_user_playing_track()["item"]["artists"][0]["name"]
        newCurrentTrackName = spotifyObject.current_user_playing_track()["item"]["name"]

        if spotifyObject.current_user_playing_track:
            if newCurrentTrackName != currentTrackName and newCurrentTrackArtist != CurrentTrackArtist:
                print("Song has changed")
                songChangeCheck(currentTrack, spotifyObject)

            currentTrack = newCurrentTrack
            currentTrackName = newCurrentTrackName
            CurrentTrackArtist = newCurrentTrackArtist
        else:
            print(False)

        time.sleep(2) # Change for 10 seconds for 30 seconds on real app

# MAIN
main(spotifyObject)
