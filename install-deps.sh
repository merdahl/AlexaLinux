#! /bin/bash

#wget --output-document vlc.py "http://git.videolan.org/?p=vlc/bindings/python.git;a=blob_plain;f=generated/vlc.py;hb=HEAD"
apt-get update
apt-get install libasound2-dev memcached python-pip python-alsaaudio mplayer -y
pip install -r requirements.txt

echo "Dependencies have been installed"
