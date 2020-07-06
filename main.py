#------------#
#  IMPORTS   #
#------------#
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time
import sqlite3
from sqlite3 import Error


#----------------------#
#   GLOBAL VARIABLES   #
#----------------------#

# Setup connection to database and create cursor
conn = sqlite3.connect('trackDatabase.db') #TODO: Maybe put the DB somewhere that wont annoy the user
c = conn.cursor() 


# Set the spotify username manually however can be done by (username = sys.argv[1]  Spotify name in command line after runnong pythong e.g. "python main.py usernameHere")
# Set the scope of the app, essentially just plugging in the functions wanting to be used for the program
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing' 


#----------------#
#   INIT/SETUP   #
#----------------#

# Try: Erase cache and prompt user permission
# Set spotifyObject to the authenticated token
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

# Create the database if not already created then commit and close the connection
c.execute("""CREATE TABLE IF NOT EXISTS songInfo (
    trackID TEXT,
    skipCount INTEGER,
    playlist TEXT
);""")

conn.commit()
# conn.close()


#---------------#
#   FUNCTIONS   #
#---------------#

# removeFromPlaylist() will remove the song from the current playlist and add it to another titled "skipped tracks"
def removeFromPlaylist(trackID):
    c.execute("INSERT INTO songInfo (trackID, skipCount) VALUES (?, ?);", (trackID, +1))
    conn.commit()

# This functions main purpose is to finalise whether the track has been skipped or not
# Once it finds out whether the track was skipped or not it will either do nothing or add the song to a database
# It will then run the function removeFromPlaylist() (See removedFromPlaylist() comment to see what it does)
def songChangeProcess(currentTrack, spotifyObject):
    trackProgress = currentTrack["progress_ms"]
    trackID = currentTrack["item"]["id"]
    track_duration = spotifyObject.track(trackID)['duration_ms']

    if (track_duration - trackProgress) < 30000: # change 30 seconds to a percentage of the song
        print("Track passed")
    else:
        print("Track skipped")
        removeFromPlaylist(trackID)


# This functions purpose is to detect if the song is skipped then send off the results to songChangeProcess() to decide
# what happens from that point onwards. 
# It starts by setting everything to brand new variables (these will be used for comparison later) then it will assign a 
# new set of variables the current playing songs data and compare if "current" == "newCurrent". 
# If it has assume the track is skipped and chuck the data into songChangeProcess() for double checking, if not do nothing for
# x amount of seconds then compare again.
def songChangeCheck(userTime):
    currentTrackName = spotifyObject.current_user_playing_track()["item"]["name"]
    currentTrack = spotifyObject.current_user_playing_track()
    currentTrackArtist = spotifyObject.current_user_playing_track()["item"]["artists"][0]["name"]

    while True:
        newCurrentTrack = spotifyObject.current_user_playing_track()
        newCurrentTrackArtist = spotifyObject.current_user_playing_track()["item"]["artists"][0]["name"]
        newCurrentTrackName = spotifyObject.current_user_playing_track()["item"]["name"]

        if spotifyObject.current_user_playing_track:
            if newCurrentTrackName != currentTrackName and newCurrentTrackArtist != currentTrackArtist:
                print("Song has changed")
                songChangeProcess(currentTrack, spotifyObject)

            currentTrack = newCurrentTrack
            currentTrackName = newCurrentTrackName
            currentTrackArtist = newCurrentTrackArtist
        else:
            print(False)

        time.sleep(userTime) # Change for 10 seconds for 30 seconds on real app

def main(spotifyObject):
    userTime = int(input("Enter the time distance between each song check: "))
    songChangeCheck(userTime)


#----------#
#   MAIN   #
#----------#
main(spotifyObject)
conn.close()
