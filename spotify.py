#!/usr/bin/python

###########################################################
##  Script to retrieve spotfiy token
##
##  Author: Emilio Zand - @EmilioZand
##
###########################################################


####
# Load libraries
####
import spotipy
import spotipy.util as util
import configparser

####
# System Config
####
config = configparser.ConfigParser()
config.read('config.ini')

####
# Configuration for Spotify
####
sp = spotipy.Spotify()
scope = 'user-read-currently-playing user-read-playback-state'
token = util.prompt_for_user_token(config['SPOTIFY']['USERNAME'], scope,client_id=config['SPOTIFY']['CLIENT_ID'] ,client_secret=config['SPOTIFY']['CLIENT_SECRET'] , redirect_uri=config['SPOTIFY']['REDIRECT_URI'])
if token:
    sp = spotipy.Spotify(auth=token)
    print ("Spotify authenticated for user " + config['SPOTIFY']['USERNAME'])
    now_playing = sp.current_user_playing_track()
else:
    print ("Can't get token for user " + config['SPOTIFY']['USERNAME'])