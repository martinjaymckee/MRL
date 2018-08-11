#### Mars Robotics Laboratory (MRL) Update
The Mars Robotics Laboratory (MRL) is a simulation of controlling rovers on the Martian surface at the Space Foundation's Discovery Center (in Colorado Springs, CO).  The first iteration of the (very popular) rovers have been made of Legos Minstorm components and they have served well.  There are a number of issues both with the hardware and the software that would be nice to correct in a new version of the MRL systems, however.  This repository will contain not only design files for the new rovers (mechanical and electrical), it will also contain the software to run them.

## Documentation
This repository includes some initial design documentation which is working toward a new control interface for the rovers.  The file mrl_control_methodology.pdf is an outline of the current control system, some identified issues and some possible solutions along with some features that would be nice to add.

## Control System
The new software system is being designed in expectation that the new rovers will have a Raspberry Pi as their main brain.  As such, the control will via a web interface.  The control system is being written in Python using the Flask framework, Mako templates, Socket.IO (communications) and P5.js (graphics).  Currently the dependencies of the code are:
  * Flask
  * Flask-Socket.IO
  * Flask-Mako
  * Gevent
  
Once these dependencies are met, the test program can be run using the command:

python3 server.py

This will start a server running on localhost (127.0.0.1), port 5000.  In the browser, connect with https://localhost:5000 to ensure that all functionality (future video streaming) works correctly.


