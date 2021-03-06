# Spotify Indicator

Shows currently playing song on [Spotify for Linux](https://www.spotify.com/us/download/linux/):

Playing:  
![](./sceenshots/playing.png)

Paused:  
![](./sceenshots/paused.png)

Menu:  
![](./sceenshots/menu.png)

Features:
 - scroll up/down on the icons plays next/previous song
 - toggle playback by clicking on the menu item
 - icon color shows the playback status: green - playing, white - paused.
 
## Prerequisite

Python3
 
## Installation

Install [sp](https://gist.github.com/wandernauta/6800547) - script to control spotify playback.
Then clone the repo, install requirements (`pip3 install -r requirements.txt`) and then execute install.sh with sudo privilege.
Then simply run `spotify-indicator`. To start the script automatically add it to the list of startup applications.