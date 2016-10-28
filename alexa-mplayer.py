#! /usr/bin/env python

import alsaaudio
import alsabuttonrecord
import creds
import json
import os
import random
import re
import requests
import signal
import subprocess
import sys
import time

from memcache import Client

"""
Copyright (c) <2016> <Michael Erdahl>

credits:

Sam Machin (AlexaPi)

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

"""

# ctrl-c handler
def signal_handler(signal, frame):
    print "User pressed ctrl-c, exiting\n"
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Setup
servers = ["127.0.0.1:11211"]  # memcached local server
mc = Client(servers, debug=1)
path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))

def internet_on():
    print "Checking Internet Connection"
    try:
        r = requests.get('https://api.amazon.com/auth/o2/token')
        print "Connection OK"
        return True
    except:
        print "Connection Failed"
    return False

def gettoken():
    token = mc.get("access_token")
    if token:
        return token
    else:
        try:
            payload = {"client_id" : Client_ID,
                       "client_secret" : Client_Secret,
                       "refresh_token" : refresh_token,
                       "grant_type" : "refresh_token", }
        except:
            raise RuntimeError("refresh_token not found - check creds")

        url = "https://api.amazon.com/auth/o2/token"
        r = requests.post(url, data = payload)
        resp = json.loads(r.text)
        mc.set("access_token", resp['access_token'], 3570)
        return resp['access_token']
		
def alexa(recording):
    url = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'
    headers = {'Authorization' : 'Bearer %s' % gettoken()}
    d = {
   		"messageHeader": {
       		"deviceContext": [
           		{
               		"name": "playbackState",
               		"namespace": "AudioPlayer",
               		"payload": {
                   		"streamId": "",
        			   	"offsetInMilliseconds": "0",
                   		"playerActivity": "IDLE"
               		}
           		}
       		]
		},
   		"messageBody": {
       		"profile": "alexa-close-talk",
       		"locale": "en-us",
       		"format": "audio/L16; rate=16000; channels=1"
   		}
	}
    with open(recording) as inf:
		files = [
				('file', ('request', json.dumps(d), 'application/json; charset=UTF-8')),
				('file', ('audio', inf, 'audio/L16; rate=16000; channels=1'))
				]	
		r = requests.post(url, headers=headers, files=files)

    if r.status_code == 200:
		for v in r.headers['content-type'].split(";"):
			if re.match('.*boundary.*', v):
				boundary =  v.split("=")[1]
		data = r.content.split(boundary)
		for d in data:
			if (len(d) >= 1024):
				audio = d.split('\r\n\r\n')[1].rstrip('--')
		with open(path+"response.mp3", 'wb') as f:
			f.write(audio)

		resp = '{}response.mp3'.format(path)
		subprocess.check_call(["mplayer", "-quiet", resp])
	
    else:
        print "Server sent unexpected status code -", r.status_code		

if __name__ == "__main__":
    print "AlexaLinux Demo"    
    while internet_on() == False:
        time.sleep(1)
            
    token = gettoken()
    
    recording = None
    if len(sys.argv) == 2:
        recording = sys.argv[1]
        print "Using recording", recording
    
    else:
        recording = path+'recording.wav'
        alsabuttonrecord.record(recording)

    alexa(recording)


