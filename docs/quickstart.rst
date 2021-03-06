.. _quickstart:
    
Quick start
===========

For this *quick start* I'm assuming you're using a Debian
based operating system (either the latest Raspbian or Ubuntu 15.04 or later)
and that you are using firmware 1.13 or greater (that is, you have applied the
update at https://github.com/pimoroni/flotilla-pre).

These prerequisites ensure that you have a recent enough Python for stuff to
work (3.4 or greater) and that the Flotilla Dock has had the majority of its
initial bugs ironed out (and that it speaks at the right speed).

.. _quickstart-permissions:

Permissions
-----------

First we need to get the permissions right. The Flotilla connects via a serial
connection (albeit over USB), and by default on Debian based systems only the
**root** user and members of the **dialout** group can access the serial ports.
Rather than have **blackpearl** users run everything as root I recommend that
you add your user to the **dialout** group instead.

On Raspbian you will usually be logging in as the ``pi`` user, so I use this
user name as the example. You should replace ``pi`` with whichever user you
intend to use **blackpearl** as. In a terminal type the following::
  
  sudo usermod -a -G dialout pi
  
Then logout and log back in again.

.. _quickstart-prerequisites:

Prerequisites
-------------

Next we need to install the prerequisite packages from the operating system.
**blackpearl** installs all of its own python packages in a virtual environment,
but there are some packages we need before we begin::
  
  sudo apt-get install python-virtualenv python3-dev git-core

.. _quickstart-installation:

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

.. note:: I'll go through what each of those lines above means in more detail
          on the :doc:`installation page </installation>`. The most
          important bit will be what on earth ``virtualenv`` is if you've never 
          come across it before. Fear not!

.. _quickstart-connect-hardware:

Connect the hardware
--------------------

Make sure that your Flotilla is connected to a USB socket on your machine, and
that a touch and a rainbow are attached to it. The three blue LEDs on the dock
should be on, one of them pulsing gently.

.. _quickstart-test:

Test
----

Back in your terminal (which you left untouched, didn't you?!) now type::
  
  python blackpearl/examples/gettingstarted.py
  
You should see some output to the terminal along the lines of::
  
  Flotilla is connected.
  INFO : b'# Flotilla ready to set sail..'
  INFO : b'# Version: 1.13'
  INFO : b'# Serial: 18000f0035573132313503'
  INFO : b'# User: Unnamed'
  INFO : b'# Dock: Unnamed'
  INFO : b'# SRAM: 1379 bytes'
  INFO : b'# Loop: 0ms (0us) 544fps'
  INFO : b'# Channels:'
  INFO : b'# - 0'
  INFO : b'# - 1 - rainbow (0x54)'
  INFO : b'# - 2'
  INFO : b'# - 3'
  INFO : b'# - 4'
  INFO : b'# - 5'
  INFO : b'# - 6 - touch (0x2c)'
  INFO : b'# - 7'
  Found a rainbow on channel 2
  Found a touch on channel 7
  INFO : All requirements met \o/

Once you see the string ``All requirements met \o/`` go past we're ready.

Press button 1. The rainbow goes red! Press button 2. The rainbow goes green!
Press button 3. The rainbow goes blue! Press button 4. The rainbow turns off!

Press ``ctrl-c`` on your keyboard and the script will stop.

Congratulations, **blackpearl** is installed and working!

(if of course this didn't work you may want to try the :doc:`troubleshooting
installation page </troubleshooting>`)
