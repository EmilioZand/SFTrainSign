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
import requests
import sys

my_zip = 94122
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
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

def getWeather():
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

####
# Call the Function(s) to create content and write this to the Matrix
####

try:
    image = getWeather()
    image.show()
except KeyboardInterrupt:
    sys.exit(0)