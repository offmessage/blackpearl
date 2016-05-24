.. _flotilla:

The Flotilla itself
===================

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/flotilla.py

**Source code** `blackpearl/things/flotilla.py`__

__ source-code_

This module provides all of the necessary wiring to connect to the Flotilla
hardware module, and to receive updates from the connected modules (like the
light sensors, the matrix, and so on).

This is the bit that makes the most of Twisted's asyncronous library.
**blackpearl** uses Twisted's SerialPort and LineReceiver classes to do all of
the heavy lifting; **blackpearl** just piggybacks on that and does Flotilla
specific things.

Most of the code is internally facing (you don't really need to know what's
going on in there), but if you do want to get down and dirty and use it
directly the things you're really going to care about are defined below.

.. function:: .flotillaCommand(command)
   
   Sends a command to the Flotilla.
   
   ``command`` must be Python 3 bytes (e.g ``b'v'``). Available commands are:
   
    * **d** (*debug*): Asks the Flotilla to send back details information about
      itself. Returns 11 lines, including the firmware version and
      what's connected to each channel
    * **v** (*version*): Asks the Flotilla to send back simple information
      about itself. Returns 5 lines, including the firmware version, the
      named user, and the dock name
    * **n** (*name*): Two options: ``n u <user name>`` sets the user name of
      the dock. ``n d <dock name>`` sets the name of the dock itself. The 
      maximum length of both names is eight characters
    * **e** (*enumerate*): List all of the connected modules. Returns one line
      for each connected module in the form ``c <channel_number>/<module_name>``
      in the same way that you would see if a module was plugged in while the
      Flotilla was already running
    * **s** (*send*): This sends a command to a particular connected module.
      See the documentation for each module for the specifics
    * **p** (*power*): Two options: ``p 0`` turns the power to all connected
      modules off, while ``p 1`` turns the power to all connected modules on


.. function:: .connectedModules(type_=None)
   
   Asks the Flotilla Python code to return which modules are connected. Rather
   than simply asking the Flotilla hardware to list what's connected (as
   ``FlotillaClient.flotillaCommand(b'e')`` would) this returns python representations
   of the connected modules that can be manipulated and used.
   
   If you pass ``type_`` (as a string, e.g. ``"motor"``) it will filter the list
   and only return the connected modules of the specified type.
   
.. function:: .firstOf(type_)
   
   Asks the Flotilla to return the python representation of the first instance
   of the give type (e.g. ``"motor"``). First is defined as the one connected
   to the lowest numbered port on the Flotilla hardware.
   
.. warning:: Importantly **blackpearl**'s ``FlotillaClient`` class expects and
             relies on there being a **blackpearl** project instance handed to
             its ``.run()`` method so you will have to craft your direct usage
             carefully.

