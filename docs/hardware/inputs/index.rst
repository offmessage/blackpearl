.. _inputs:
    
Flotilla Hardware Inputs
========================

**blackpearl** provides lightweight wrappers around the hardware inputs that
come with the Flotilla kits. It's not possible to change the inputs through
Python code, but these modules provide some sanitisation of the input, as well
as some convenience methods for calculating useful things from the raw data
(like RGB values from the colour sensor and compass headings from the motion
sensor).

Each of the modules is documented below:

.. toctree::
    :maxdepth: 2
    
    dial.rst
    slider.rst
    joystick.rst
    touch.rst
    light.rst
    colour.rst
    weather.rst
    motion.rst
    