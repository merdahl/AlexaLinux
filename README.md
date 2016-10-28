Acknowledgements
================
Portions of this project are based on the work of Sam Munchin and his
AlexaPi project.  This represents a cut-down version of his work to establish
a bare-minimum cross-platform means to access the Alexa Voice Service (AVS).


Installation instructions
=========================
Before talking to Alexa, there are three steps to complete:

1. Create an Amazon developer account, then register your Alexa device.
Please check out NovaSpirit's video on YouTube to take care of these 
requirements - ignore anything specific to the Raspberry Pi.

2. Run the install-deps.sh script to grab the necessary dependencies for your
system.  Note, these are for a Debian-based OS.  Others systems will require
a different method to get these dependencies.

3. Run the generate-creds.sh script to get the "refresh token" required to
access Amazon Alexa Voice Service.  You will be connecting to your device's
IP address at port 5000.  E.g, if your device has ip address 192.168.1.10,
use a device on the same subnet to connect to http://192.168.1.10:5000 (NOTE:
must be HTTP, NOT HTTPS).  If you see a "sorry" message from Amazon, you
have entered an incorrect value when creating creds.py - everything must match
exactly.

Getting Started
===============
This project is intended to initiate a single interaction with AVS.  If you
want to carry on interactive conversations, put "start" into an infinite
loop.

The interaction model with Alexa is very simplistic and is done this way to keep
the code short.  As a consequence, you can only ask Alexa questions, but if
you tried to stream a radio channel, or music from Amazon, it will not work
because nothing is put in place to capture the streaming audio URL.  For
streaming audio applications, take a look at the AlexaBeagleBone or AlexaPi
projects.

Press-and-hold a key while speaking into your microphone.  Release the key when 
your phrase is complete.  This project currently uses /dev/input/ character 
devices to initiate a recording for Alexa.  See the description under 
alsabuttonrecord.py below for more information about how to set this up on your
system.  There are two problems with this approach: 1) requires sudo 2) if you
use your keyboard, the screen will be filled with chars while recording.

Notes
=====
This can be ran on a PC, or on an embedded platform.

alexa-mplayer.py
----------------
Main script to communicate with Amazon Alexa Voice Service.  The script will 
return after a single iteraction, but could easily be modified to loop forever.

alsabuttonrecord.py
-------------------
Helper script that records from microphone to .wav file for AVS to process.

Use 'evtest' program to determine mapping of char device handle of desired
input source (/dev/input/input[0..n])

On my PC, /dev/input/input4 is mapped to the physical keyboard.
On the AM335x GP EVM, the matrix keypad located on the LCD daughterboard is
mapped to /dev/input/input1.

auth_web.py
-----------
Helper script to get refresh token from AMZN - called by generate-creds.sh

creds.py
--------
Credentials necessary to access AVS.  Use "generate-creds.sh" script to generate 
new credentials.  Note, it is advisable to clear out any previous credentials
first.  Also do not make this publicly available :)

generate-creds.sh
-----------------
Generates credentials file with necessary fields required to access AVS 

install-deps.sh
---------------
Installs necessary dependencies for this project

requirements.txt
----------------
Used by python pip to pull down necessary python libraries
