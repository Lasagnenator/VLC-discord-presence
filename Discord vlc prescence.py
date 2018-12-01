#Discord vlc prescence

import NowPlaying
import pypresence
import time
import datetime

getInfo = NowPlaying.getInfo

getInfo()
f = open("./NowPlaying.txt", "r")
old_song = f.read()
f.close()


def getTimestamp():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

def getTimes():
    timeFile = open("./TimeFile.txt", "r")
    pos, length = timeFile.read().split("\n")
    return int(pos), int(length)

def songChanged():
    global old_song
    getInfo()
    f = open("./NowPlaying.txt", "r")
    new_song = f.read()
    f.close()
    if old_song!=new_song:
        old_song = new_song
        return True
    return False

def update():
    #details = old_song
    pos, length = getTimes()
    print(pos, length)
    start = getTimestamp()-pos
    end =getTimestamp()+(length-pos)
    artist, title = old_song.split(' - ')
    details = title
    state = "by "+artist
    large_image = "904px-vlc_icon"
    #Activity.started_at(pos)
    #Activity.end_in(length-pos)
    #print(details, start, large_image)
    Presence.update(details = details,
                    state = state,
                    large_image = large_image,
                    start = start,
                    end = end)

Presence = pypresence.Presence(client_id = "518331179422973962")

Presence.connect()
update()

while True:
    if songChanged():
        update()
    time.sleep(15)
