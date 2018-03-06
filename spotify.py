#!/usr/bin/python

import spotipy
import spotipy.util as util
import requests

####
# Configuration for Spotify
####
sp = spotipy.Spotify()
scope = 'user-read-currently-playing user-read-playback-state'
token = util.prompt_for_user_token('ezmang',scope,client_id='225f80f5e8cb417e844ddd710eef373e',client_secret='d3971be2179343e0af3376b03fb43202',redirect_uri='http://localhost/')
if token:
    sp = spotipy.Spotify(auth=token)
    print sp.current_user_playing_track()
else:
    print "Can't get token for ezmang"
