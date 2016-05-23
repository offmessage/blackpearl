.. messages:
    
Messages
========

Messages are the core of how the various bits of **blackpearl** communicate with
each other. Anything like the Flotilla is *event driven* - the system waits for
events (inputs) from external influences, be that user input (like pressing a
button on the touch), sensor input (like the temperature changing) or system
input (like a tick from a clock, or a sine wave).

The programs that you write to use **blackpearl** listen for messages being
broadcast by other bits of the system.

I've tried to use the same terminology as the excellent Scratch so that
younger coders will feel at home with what's going on here. Essentially anything
can ``broadcast`` a message, and anyone who has said that they are listening for
a message of that type will ``receive`` it.

