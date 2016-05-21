"""
=======================================
Black Pearl: For twisted little pirates
=======================================

modules/

Modules are the software components that we deal with day to day. They take
input and create output. These are the things that users should be subclassing
for their projects.
"""

from .base import Module
from .timers import Clock
from .colour import Colour
from .dial import Dial
from .joystick import Joystick
from .motion import Motion
from .slider import Slider
from .timers import Timer
from .touch import Touch
from .weather import Weather
