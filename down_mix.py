#!/usr/bin/python
import os
import requests
from sys import argv
import re
from bs4 import BeautifulSoup
import random
import unicodedata
import string
import datetime

BASE_URL= 'http://www.youtube.com/watch?v='
EXT = '.mp3'
TEMP_VID = '.youtube-dl-%s.flv'
LOWER = 100000
UPPER = 999999
PARSE_ERROR = '''This URL page is created dynamically and causes problems for detection\r\n
                    There is an experimental selenium solution but requires selenium and \r\n
                    ChromeDriver in order to render the page dynamically and then strip the \r\n
                    source.\r\n
                '''
def clean_name(title):
    #some stackoverflow fun, adapted of course
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in valid_chars)

def selenium(url):
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    playlist = re.compile('<ol id=\"watch7-playlist-tray\" class=\"yt-uix-scroller\" .+?</ol>',re.DOTALL).findall(driver.page_source)
    driver.close()
    return playlist

def plain_get(url):
    r = requests.get(url)
    playlist = re.compile('<ol id=\"watch7-playlist-tray\" class=\"yt-uix-scroller\" .+?</ol>',re.DOTALL).findall(r.text)
    return playlist

def create_mp3s(playlist):
    originalDir = os.getcwd()
    newDir = os.path.join(originalDir, str(datetime.datetime.now()))
    if not os.path.exists(newDir):
        os.mkdir(newDir)
    os.chdir(newDir)

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

def offer_selenium(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def main(use_selenium=False):
    url = raw_input("Enter your mix URL:")

    if use_selenium:
        playlist = selenium(url)
    else:
        playlist = plain_get(url)

    if playlist:
        create_mp3s(playlist)
    else:
        print PARSE_ERROR
        if not use_selenium and offer_selenium(prompt='Try Selenium?',resp=True):
            main(use_selenium=True)
        else:
            print '''Sorry Youtube may have changed things or your using this outside of its\r\n
                     intended use if you feel like you were feeding a valid URL into this\r\n
                     app you may submit a bug, include your URL'''

main()



