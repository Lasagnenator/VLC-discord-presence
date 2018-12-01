# VLC-discord-presence

# Setup
See https://obsproject.com/forum/resources/vlc-nowplaying.244/ readme.txt for setup (ignore stuf about OBS)

Create a bot in discord:
1. Goto https://discordapp.com/developers/
2. Click “Create an Application.”
3. Setup the application how you want, give it the name VLC (), and set the image to VLC's icon (you can find one anywhere).
4. Add an image asset that is the same as the icon
5. Right under the name of your application, locate your Client ID. You will need this later.
6. Lastly, save your application.

Goto `Discord vlc presence.py` and change ClientID (near the bottom) to the bot's clientID

Goto `Discord vlc presence.py` and at line 44 change ImageName to the name of the uploaded image

# Usage
Run `Discord vlc presence.py`

Run VLC and play music or whatever

And of course, have discord open!

# Requirements
pypresence 3.3.0+
requests 2.19.1+

# Acknowledgements
NowPlaying.py was not created by me (however, I have edited it slightly). https://obsproject.com/forum/resources/vlc-nowplaying.244/

