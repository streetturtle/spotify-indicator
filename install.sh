#!/usr/bin/env bash

mkdir -p /usr/share/spotify-indicator
cp ./spotify-indicator.py /usr/share/spotify-indicator
cp ./Spotify_Icon_RGB_Green.png /usr/share/spotify-indicator
cp ./Spotify_Icon_RGB_White.png /usr/share/spotify-indicator

chmod +x /usr/share/spotify-indicator/spotify-indicator.py
ln -sf /usr/share/spotify-indicator/spotify-indicator.py /usr/local/bin/spotify-indicator