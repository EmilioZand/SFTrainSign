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
scope = 'user-read-currently-playing user-read-playback-state'

class Spotify:
    now_playing = None
    def __init__(self):
        self.sp = spotipy.Spotify()
        self.token = util.prompt_for_user_token(config['SPOTIFY']['USERNAME'], scope,client_id=config['SPOTIFY']['CLIENT_ID'] ,client_secret=config['SPOTIFY']['CLIENT_SECRET'] , redirect_uri=config['SPOTIFY']['REDIRECT_URI'])
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
            print ("Spotify authenticated for user " + config['SPOTIFY']['USERNAME'])
            now_playing = self.sp.current_user_playing_track()
        else:
            print ("Can't get token for user " + config['SPOTIFY']['USERNAME'])
    def refresh_token(self):
        self.sp = spotipy.Spotify()
        self.token = util.prompt_for_user_token(config['SPOTIFY']['USERNAME'], scope,client_id=config['SPOTIFY']['CLIENT_ID'] ,client_secret=config['SPOTIFY']['CLIENT_SECRET'] , redirect_uri=config['SPOTIFY']['REDIRECT_URI'])
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
            self.now_playing = self.sp.current_user_playing_track()
            print ("Spotify authenticated for user " + config['SPOTIFY']['USERNAME'])
        else:
            print ("Can't get token for user " + config['SPOTIFY']['USERNAME'])
    def get_now_playing(self):
        try:
            self.now_playing = self.sp.current_user_playing_track()
        except: 
            self.now_playing = None
            self.refresh_token()
        return self.now_playing
