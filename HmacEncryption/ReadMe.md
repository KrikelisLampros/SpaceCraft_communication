To run the code provided please run the install.sh file.  Then read the .pdf File and follow the instructions .

The base station transmits  a specific position(x,y) for a spacecraft in 2D map.
In the spacecraft_inst you will find how each spacecraft handles uniquely the transmitted message.
in side the spacecraft_inst there is a function which allow the spacecraft to log and save the messages .
In the listen.py file there is new script which listen all the interactions between base Station  and Spacecraft  and logs only the successful ones .

~*Note*~ We encrypt the interaction between Base Station and Spacecraft with H mac function.
