#!/usr/bin/python

###########################################################
##  Script for sending text to LED Matrices
##
##  Author: Emilio Zand - @EmilioZand
##
###########################################################

####
# Load libraries
####
from PIL import Image, ImageDraw, ImageFont, ImageOps
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from decimal import Decimal, ROUND_HALF_UP
import time
import requests
import json
import sys
import logging
import logging.handlers
import os
import configparser
import spotipy
import spotipy.util as util
import googlemaps

####
# System Config
####
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/var/log/matrix.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
config = configparser.ConfigParser()
config.read('config.ini')

####
# Configuration for the matrix
####
options = RGBMatrixOptions()
options.rows = config['MATRIX']['ROWS']
options.cols = config['MATRIX']['COLS']
options.chain_length =  config['MATRIX']['CHAIN_LENGTH']
options.hardware_maping = config['MATRIX']['HARDWARE_MAPPING']
options.brightness = config['MATRIX']['HARDWARE_MAPPING']

####
# Configuration for Spotify
####
sp = spotipy.Spotify()
scope = 'user-read-currently-playing user-read-playback-state'
token = util.prompt_for_user_token(config['SPOTIFY']['USERNAME'], scope,client_id=config['SPOTIFY']['CLIENT_ID'] ,client_secret=config['DEFAULT']['CLIENT_SECRET'] , redirect_uri=config['SPOTIFY']['REDIRECT_URI'])
if token:
    sp = spotipy.Spotify(auth=token)
    print "Spotify authenticated for user ezmang"
else:
    print "Can't get token for ezmang"

####
# Configuration for Gmaps
####
gmaps = googlemaps.Client(key=config['LOCATION']['GOOGLE_API'])

####
# Variables
####
my_zip = config['LOCATION']['ZIP']   # US Zip Code used in the weather module
origin = config['LOCATION']['HOME']
destination = config['LOCATION']['WORK']
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
bustime_api_key = config['MUNI']['API_KEY']
stops = config['MUNI']['STOPS']
on_hour = config['MATRIX']['ON_HOUR']
off_hour = config['MATRIX']['OFF_HOUR']

####
# Fonts
####
display = ImageFont.truetype("fonts/Display.ttf", 10)
eightbit = ImageFont.truetype("fonts/8-bit-wonder.ttf", 8)
bitty = ImageFont.truetype("fonts/Bittypix.otf", 8)
minecraft = ImageFont.truetype("fonts/Minecraft.ttf", 16)
vcr = ImageFont.truetype("fonts/vcr-ocd-mono.ttf", 10)
pixeled = ImageFont.truetype("fonts/Pixeled.ttf", 10)
pressStart = ImageFont.truetype("fonts/PressStart2P.ttf", 8)
wendy = ImageFont.truetype("fonts/wendy.ttf", 5)
visitor = ImageFont.truetype("fonts/visitor2.ttf", 10)
pf = ImageFont.truetype("fonts/pf_tempesta_seven.ttf", 8)
minecraftia = ImageFont.truetype("fonts/Minecraftia-Regular.ttf", 8)
pixelmix = ImageFont.truetype("fonts/pixelmix.ttf", 8)
zero4b = ImageFont.truetype("fonts/zero4b.ttf", 8)
pixelated = ImageFont.truetype("fonts/pixelated.ttf", 8)

####
# Methods
####

def round_decimal(x):
    return Decimal(x).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


def parseTrainsJSON(trains):
    route_tag = trains['predictions']['routeTag']

    if isinstance(trains['predictions']['direction'], list):
        if isinstance(trains['predictions']['direction'][0]['prediction'], list):
            train1 = trains['predictions']['direction'][0]['prediction'][0]
            train2 = trains['predictions']['direction'][0]['prediction'][1]
            train1_title = trains['predictions']['direction'][0]['title'][11:]
            train2_title = trains['predictions']['direction'][0]['title'][11:]
        else:
            train1 = trains['predictions']['direction'][0]['prediction']
            train1_title = trains['predictions']['direction'][0]['title'][11:]
            train2_title = trains['predictions']['direction'][1]['title'][11:]

            if isinstance(trains['predictions']['direction'][1]['prediction'], list):
                train2 = trains['predictions']['direction'][1]['prediction'][0]
            else:
                train2 = trains['predictions']['direction'][1]['prediction']
    else:
        if isinstance(trains['predictions']['direction']['prediction'], list):
            train1 = trains['predictions']['direction']['prediction'][0]
            train2 = trains['predictions']['direction']['prediction'][1]
            train1_title = trains['predictions']['direction']['title'][11:]
            train2_title = trains['predictions']['direction']['title'][11:]
        else:
            train1 = trains['predictions']['direction']['prediction']
            train1_title = trains['predictions']['direction']['title'][11:]
            train2_title = ""
            train2 = {'minutes': '' }

    if isinstance(train1, list):
        train1 = train1[0]
    if isinstance(train2, list):
        train2 = train2[0]

    return [{'line': route_tag, 'destination': train1_title, 'minutes': train1['minutes']},
              {'line': route_tag, 'destination': train2_title, 'minutes': train2['minutes']}]

def getNextTrainsImage():
    # This function accesses the San Francisco SFMTA
    # This returns an object with the next 2 trains for a stop
    requests.packages.urllib3.disable_warnings()
    nextbus = requests.get("http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=sf-muni&r=N&s=5197&useShortTitles=true")
    nextbus_json = nextbus.json()

    trains = parseTrainsJSON(nextbus_json)

    trainImage = Image.new("RGB", (128, 32))  # Can be larger than matrix if wanted!!
    trainDraw = ImageDraw.Draw(trainImage)  # Declare Draw instance before prims

    trainDraw.ellipse((5, 3, 15, 13), fill=(4, 82, 156))
    trainDraw.ellipse((5, 19, 15, 29), fill=(4, 82, 156))
    trainDraw.text((8,3), trains[0]['line'], font=vcr, fill=(0, 0, 0))
    trainDraw.text((8,19), trains[1]['line'], font=vcr, fill=(0, 0, 0))
    trainDraw.text((19,5), trains[0]['destination'], font=zero4b, fill=(0, 255, 255))
    trainDraw.text((19,20), trains[1]['destination'], font=zero4b, fill=(0, 255, 255))
    trainDraw.text((97,4), trains[0]['minutes'], font=pixelmix, fill=(255, 0, 255))
    trainDraw.text((97, 19), trains[1]['minutes'], font=pixelmix, fill=(255, 0, 255))
    trainDraw.text((110,3), "min", font=pixelmix, fill=(0, 255, 255))
    trainDraw.text((110,19), "min", font=pixelmix, fill=(0, 255, 255))

    return trainImage

def getCryptoImage():
    requests.packages.urllib3.disable_warnings()
    coinmarketcap = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=4")
    cryptos = coinmarketcap.json()
    cryptoImage = Image.new("RGB", (128, 32))  # Can be larger than matrix if wanted!!
    cryptoDraw = ImageDraw.Draw(cryptoImage)  # Declare Draw instance before prims

    cryptoDraw.text((3,3), cryptos[0]['symbol'], font=pixelmix, fill=(0, 255, 255))
    cryptoDraw.text((24,3), cryptos[0]['price_usd'][:7], font=pixelmix, fill=(0, 255, 255))
    cryptoDraw.text((67,3), cryptos[1]['symbol'], font=pixelmix, fill=(255, 0, 255))
    cryptoDraw.text((89,3), cryptos[1]['price_usd'][:7], font=pixelmix, fill=(255, 0, 255))
    cryptoDraw.text((3,18), cryptos[2]['symbol'], font=pixelmix, fill=(255, 0, 255))
    cryptoDraw.text((24,18), cryptos[2]['price_usd'][:7], font=pixelmix, fill=(255, 0, 255))
    cryptoDraw.text((67,18), cryptos[3]['symbol'], font=pixelmix, fill=(0, 255, 255))
    cryptoDraw.text((89,18), cryptos[3]['price_usd'][:7], font=pixelmix, fill=(0, 255, 255))

    return cryptoImage

def WeatherUpdate():
    headers = {'User-Agent': ua}
    url = 'http://api-ak.wunderground.com/api/c991975b7f4186c0/forecast/v:2.0/q/zmw:'+str(my_zip)+'.1.99999.json'
    try:
        weather_req = requests.get(url, headers=headers)
        all_weather = weather_req.json()
        if 'error' in all_weather['response']:
            print 'ERROR! %s' % all_weather['response']['error']['description']
            return '* Weather ERROR *'
        else:
            return all_weather['forecast']['days'][0]['summary']
    except:
        return '* Weather ERROR - Web Call *'

def getWeatherImage():
    weatherImage = Image.new("RGB", (128,32))
    weatherDraw = ImageDraw.Draw(weatherImage)
    weatherText = WeatherUpdate()
    weatherIcon = Image.open('weather/' + weatherText['icon'] + '.png').convert('RGBA')
    weatherIcon = weatherIcon.resize((18, 18))
    weatherImage.paste(weatherIcon, (4, 15))
    weatherDraw.text((3,3), "High:", font=minecraft, fill=(255,0,255))
    weatherDraw.text((43,3), str(weatherText['high']), font=minecraft, fill=(255,0,255))
    weatherDraw.text((67,3), "Low:", font=minecraft, fill=(0,255,255))
    weatherDraw.text((107,3), str(weatherText['low']), font=minecraft, fill=(0,255,255))
    weatherDraw.text((25,19), str(weatherText['condition']), font=pixelmix, fill=(0,255,255))

    return weatherImage

def getSpotifyImage():
    now_playing = sp.current_user_playing_track()
    if now_playing and now_playing['is_playing']:
        title = now_playing['item']['name']
        artists = ''
        count = 0
        for artist in now_playing['item']['artists']:
            if count > 0:
                artists += ', '
            artists += (artist['name'])
            count += 1

        spotifyImage = Image.open("images/spotify.png").convert('RGB')
        spotifyDraw = ImageDraw.Draw(spotifyImage)
        spotifyDraw.text((40,3), title, font=minecraftia, fill=(0, 255, 255))
        spotifyDraw.text((40,18), artists, font=minecraftia, fill=(255, 0, 255))
        return spotifyImage
    else:
        return None

def getDriveTime():
    now = datetime.now()
    directions_result = gmaps.directions(origin, destination, departure_time=now)
    return directions_result[0]['legs'][0]['duration_in_traffic']['text']

def getDriveImage():
    now = datetime.now()
    if now.hour > 12 and now.weekday() > 4:
        return None

    driveImage = Image.new("RGB", (128,32))
    driveDraw = ImageDraw.Draw(driveImage)
    driveTime = getDriveTime()
    carIcon = Image.open('images/car.png')
    driveImage.paste(carIcon, (5, 6))
    driveDraw.text((50,1), "Time to Work:", font=pf, fill=(0,255,255))
    driveDraw.text((65,16), driveTime, font=pf, fill=(0,255,255))
    return driveImage

def drawFPS(image):
    if image is None:
        break
    else:
        matrix.Clear()
        matrix.SetImage(image, 0, 0)
        time.sleep(10)

def checkOffHours()
    now = datetime.now()
    return (now.hour < on_hour or now.hour > off_hour)

####
# Create
####
matrix = RGBMatrix(options = options)

####
# Call the Function(s) to create content and write this to the Matrix
####

try:
    print("Press CTRL-C to stop.")
    while True:
        if checkOffHours():
            matrix.Clear()
            time.sleep(60)
        else:     
            drawFPS(getWeatherImage())
            drawFPS(getDriveImage())
            drawFPS(getNextTrainsImage())
            drawFPS(getSpotifyImage())
            drawFPS(getCryptoImage())
except KeyboardInterrupt:
    sys.exit(0)
except Exception:
    logging.exception("Exception in main()")
    exit(1)
