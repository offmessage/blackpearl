.. _messages:
    
Messages
========

Messages are the core of how the various bits of **blackpearl** communicate with
each other. **blackpearl** and the way it communicates with the Flotilla is
called *event driven* - the system waits for events from external influences, 
be that user input (like pressing a button on the touch or twiddling the dial),
sensor input (like the temperature or the light level changing) or system
input (like a tick from a clock, or a sine wave, or a web page returning).

Each of these *events* create a message that is passed around the system to any
modules that have said they are listening for them. The code that you write to
use **blackpearl** listens for messages being broadcast by other bits of the
system and reacts to them.

I've used the same terminology as `Scratch <http://scratch.mit.edu>`_ so
that coders with Scratch experience will feel at home with what's going on here.
Essentially anything can **broadcast** a message, and anyone who has said that
they are listening for a message of that type will **receive** it.

**blackpearl**'s standard messages
----------------------------------

The components within **blackpearl** send the following standard messages. You
can define your own, too (but we'll come to that later).

The Flotilla hardware inputs all send messages when something changes. These
are:

 * ``'colour'`` - the colour sensor - sends a message when the colour it can see
   changes, or when the overall light level changes
 * ``'dial'`` - the dial - sends a message when someone turns the dial
 * ``'joystick'`` - the joystick - sends a message when the joystick moves or
   when the button is pressed
 * ``'light'`` - the light sensor - sends a message when the light level changes
 * ``'motion'`` - the accelerometer and magnetometer - sends a message whenever
   the sensor is moved (in any direction, however slowly)
 * ``'slider'`` - the slider - sends a message when someone slides the slider
 * ``'touch'`` - the touch keypad - sends a message when someone presses or
   releases a button
 * ``'weather'`` - the thermometer and barometer - sends a messages whenever the
   temperature or pressure changes
 
The **blackpearl** software components send messages too:

 * ``'sawtoothwave'`` - a sawtooth wave generator - sends out regular values 
   that make up a saw tooth wave
 * ``'sinewave'`` - a sine wave generator - sends out regular values that make
   up a sine wave
 * ``'squarewave'`` - a square wave generator - sends out regular values that
   make up a square wave
 * ``'trianglewave'`` - a triangle wave generator - sends out regular values
   that make up a triangle wave
 * ``'clock'`` - a clock - sends out the current time twice a second
 
And finally the **blackpearl** system itself also sends messages:

 * ``'log'`` - Python logging messages, so that you can do cool things like make
   the rainbow go red if there's an error!
   
