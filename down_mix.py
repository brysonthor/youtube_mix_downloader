#!/usr/bin/python
import os
import requests
from sys import argv
import re
from bs4 import BeautifulSoup

BASE_URL= 'http://www.youtube.com/watch?v='
EXT = '.mp3'

r = requests.get(argv[1])
print argv[1]
playlist = re.compile('<ol id=\"watch7-playlist-tray\" class=\"yt-uix-scroller\" .+?</ol>',re.DOTALL).findall(r.text)

playlistObj = BeautifulSoup(playlist[0])

videoUrlList = []

for l in playlistObj.find_all('li'):
    videoUrlList.append((BASE_URL+l.get('data-video-id'),l.get('data-video-title')+EXT))

for v in videoUrlList:
    cmd = 'youtube2mp3 "%s" "%s"' %(v[0],v[1])
    print cmd
    os.system(cmd)












