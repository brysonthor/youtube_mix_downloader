#!/usr/bin/python
import os
import requests
from sys import argv
import re
from bs4 import BeautifulSoup
import random
import unicodedata
import string

def clean_name(title):
    #some stackoverflow fun, adapted of course
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in valid_chars)

def main():
    BASE_URL= 'http://www.youtube.com/watch?v='
    EXT = '.mp3'
    TEMP_VID = '.youtube-dl-%s.flv'
    LOWER = 100000
    UPPER = 999999
    r = requests.get(argv[1])

    playlist = re.compile('<ol id=\"watch7-playlist-tray\" class=\"yt-uix-scroller\" .+?</ol>',re.DOTALL).findall(r.text)

    playlistObj = BeautifulSoup(playlist[0])

    videoUrlList = []

    for l in playlistObj.find_all('li'):
        videoUrlList.append((BASE_URL+l.get('data-video-id'),l.get('data-video-title')+EXT))

    for v in videoUrlList:
        temp_file = TEMP_VID % random.randint(LOWER,UPPER)
        youtube_cmd = 'youtube-dl --output="%s" --format=18 "%s"' %(temp_file,v[0])
        conv_cmd = 'ffmpeg -i "%s" -acodec libmp3lame -ac 2 -ab 320k -vn -y "%s"' %(temp_file,clean_name(v[1]))
        #print temp_file,youtube_cmd,conv_cmd
        os.system(youtube_cmd)
        os.system(conv_cmd)
        os.remove(temp_file)

main()



