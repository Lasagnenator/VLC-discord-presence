#!/usr/bin/env python
#===============================================================================
# title           :NowPlaying.py
# description     :This script will create a NowPlaying.txt file that contains
#                   the info for the song that is currently being played via VLC
# author          :Tipher88
# contributors    :AbyssHunted, Etuldan
# date            :20160708
# version         :1.5.0
# usage           :python NowPlaying.py
# notes           :For this script to work you need to follow the instructions
#                   in the included README.txt file
# python_version  :2.7.10 & 3.4.3
#===============================================================================

import os, time, datetime, requests, codecs
import xml.etree.ElementTree as ET

try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
	import html

# Global variable to keep track of song info being printed and check for changes
currentSongInfo = ''

def getInfo():
    # CUSTOM: Separator can be changed to whatever you want
    separator = '   |   '
    
    nowPlaying = 'UNKNOWN'
    songTitle = 'UNKNOWN'
    songArtist = 'UNKNOWN'
    fileName = ''
    
    s = requests.Session()
    
    # CUSTOM: Username is blank, just provide the password
    s.auth = ('', 'password')
    
    # Attempt to retrieve song info from the web interface
    try:
        r = s.get('http://localhost:8080/requests/status.xml', verify=False)
        
        if('401 Client error' in r.text):
            print('Web Interface Error: Do the passwords match as described in the README.txt?')
            return
    except:
        print('Web Interface Error: Is VLC running? Did you enable the Web Interface as described in the README.txt?')
        return
    
    # Okay, now we know we have a response with our xml data in it
    # Save the response data
    root = ET.fromstring(r.content)

    # Find current position and length of song
    pos = root.find("time").text
    length = root.find("length").text
    timeFile = open("./TimeFile.txt", "w")
    timeFile.write(pos+"\n"+length)
    timeFile.close()
    
    # Loop through all info nodes to find relevant metadata
    for info in root.iter('info'):
        # Save the name attribute of the info node
        name = info.get('name')
        
        # See if the info node we are looking at is now_playing
        if(name == 'now_playing'):
            nowPlaying = info.text
        else:
            # See if the info node we are looking at is for the artist
            if(name == 'artist'):
                songArtist = info.text
            
            # See if the info node we are looking at is for the title
            if(name == 'title'):
                songTitle = info.text
            
            # See if the info node we are looking at is for the filename
            if(name == 'filename'):
                fileName = info.text
                fileName = os.path.splitext(fileName)[0]
            #if(name == 'artwork_url'):
                #artPath = info.text
    # END: for info in root.iter('info')
    
    # If the now_playing node exists we should use that and ignore the rest
    if(nowPlaying != 'UNKNOWN'):
        writeSongInfoToFile(nowPlaying, separator)
    else:
        # Make sure a songTitle and songArtist was found in the metadata
        if(songTitle != 'UNKNOWN' and
           songArtist != 'UNKNOWN'):
            # Both songTitle and song Artist have been set so use both
            writeSongInfoToFile(songTitle, separator)
        elif( songTitle != 'UNKNOWN' ):
            # Just use the songTitle
            writeSongInfoToFile(songTitle, separator)
        #elif(artPath != 'UNKNOWN'):
            #artfile = open('./ArtFile.txt', 'w', encoding='utf-8')
            #artfile.write(html.unescape(artPath))
            #artfile.close()
        elif( fileName != '' ):
            # Use the fileName as a last resort
            writeSongInfoToFile(fileName, separator)
        else:
            # This should print 'UNKNOWN - UNKNOWN' because no relevant metadata was
            #   found
            writeSongInfoToFile("No song data.", separator)
# END: getInfo()

def writeSongInfoToFile( songInfo, separator ):
    global currentSongInfo
    
    if(currentSongInfo != songInfo):
        currentSongInfo = songInfo
        print(html.unescape(currentSongInfo))
    
        # CUSTOM: The output file name can be changed
        textFile = open('./NowPlaying.txt', 'w', encoding='utf-8')
        textFile.write(html.unescape(currentSongInfo))
        textFile.close()
        
        timeStamp = '{:%H:%M:%S}:'.format(datetime.datetime.now())
    
        # CUSTOM: The output file name can be changed
        textFile = open('./NowPlaying_History.txt', 'a', encoding='utf-8')
        textFile.write(html.unescape(('%s %s%s') % (timeStamp, currentSongInfo, os.linesep)))
        textFile.close()
# END: writeSongInfoToFile( songInfo, separator )
