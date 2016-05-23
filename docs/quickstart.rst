.. quickstart:
    
Quick start
===========

In a few lines you should be able to get this code working.

First, the basics. For this *quick start* I'm assuming you're using a Debian
based operating system (either the latest Raspbian or Ubuntu 15.04 or later)
and that you are using firmware 1.13 or greater (you have applied the update at
https://github.com/pimoroni/flotilla-pre). We set these prerequisites to make
sure that you have a recent enough Python for stuff to work (3.4 or greater)
and that the Flotilla Dock has had the majority of its initial bugs ironed out
(and that it speaks at the right speed).

Permissions
-----------

First up, let's get the permissions right. The Flotilla connects via a serial
connection (albeit over USB). By default on Debian based systems only the
**root** user and members of the **dialout** group can access the serial ports.
Rather than have **blackpearl** users run everything as root I recommend that
you add your user to the **dialout** group instead.

On Raspbian you will usually be logging in as the ``pi`` user, so I use this
user name as the example. You should replace ``pi`` with whichever user you
intend to use **blackpearl** as. In a terminal type the following::
  
  sudo usermod -a -G dialout pi
  
Then logout and log back in again.

Prerequisites
-------------

Next we need to install the prerequisite packages from the operating system.
**blackpearl** installs all of its own python packages in a virtual environment,
but there are some packages we need before we begin::
  
  sudo apt-get install python-virtualenv python3-dev git-core
  
Installation
------------

I'm assuming you put all your projects in a folder in your home directory called
``projects``. So, wherever you see ``/home/pi/projects`` you should replace this
with wherever you prefer to install stuff (e.g. ``/home/andy/Documents/Flotilla``
or whatever).

In a terminal type the following::
  
  mkdir /home/pi/projects
  cd /home/pi/projects
  git clone https://github.com/offmessage/blackpearl
  cd blackpearl
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -e .
  
Leave your terminal as is while you do the next steps.

I'll go through what each of those lines above means in more detail on the
installation page.

Connection
----------

Make sure that your Flotilla is connected to a USB socket on your machine, and
that a touch and a rainbow are attached to it. The three blue LEDs on the dock
should be on, possibly pulsing gently.

Test
----

Back in your terminal (which you left untouched, didn't you?!) now type::
  
  python blackpearl/examples/touchtherainbow.py
  
You should see some output to the terminal along the lines of::
  
  PASTE IT HERE
  
Once you see the string ``All requirements met \o/`` go past we're ready.

Press button 1. The rainbow goes red! Press button 2. The rainbow goes green!
Press button 3. The rainbow goes blue! Press button 4. The rainbow turns off!

Press ``ctrl-c`` on your keyboard and the script will stop.

Congratulations, **blackpearl** is installed and working!
