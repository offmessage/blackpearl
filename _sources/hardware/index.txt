.. hardware:

Flotilla hardware things
========================

**blackpearl** provides Python wrappers around each of the hardware things that
come with the Flotilla kits.

The inputs send messages depending on events that occur (like button presses or
changes in temperature); the **blackpearl** code takes the raw output from the
dock itself and turns it into something consumable by Python code (and does
some calculations in advance, too).

The outputs take actions that your code tells them to. That might be to display
a certain pattern on the rainbow, display a letter on the matrix or move the
motors one way or another. In certain circumstances they can send messages too
(like when an animation sequence has ended).

These next pages give some real detail about the message formats that each
sends, as well as the methods that you can call to make the outputs do things.
It's likely that these pages are the ones you'll refer to the most once you've
got the basics nailed.

.. toctree::
    :maxdepth: 2

    flotilla.rst
    inputs/index.rst
    outputs/index.rst
    
