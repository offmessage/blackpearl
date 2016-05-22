"""
=======================================
Black Pearl: For twisted little pirates
=======================================

things/

Contains all the information about how to communicate with Flotilla hardware
modules and our software components.
"""


from .flotilla import FlotillaClient
from .hardware import Colour
from .hardware import Dial
from .hardware import Joystick
from .hardware import Light
from .hardware import Matrix
from .hardware import Motion
from .hardware import Motor
from .hardware import Number
from .hardware import Rainbow
from .hardware import Slider
from .hardware import Touch
from .hardware import Weather

from .software import Saw
from .software import Sine
from .software import Square
from .software import Triangle
