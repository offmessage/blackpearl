"""
=======================================
Black Pearl: For twisted little pirates
=======================================

hardware/

Contains all the information about how to communicate with Flotilla hardware
modules
"""


from .client import FlotillaClient
from .colour import ColourInput
from .dial import DialInput
from .joystick import JoystickInput
from .light import LightInput
from .matrix import MatrixOutput
from .motion import MotionInput
from .motor import MotorOutput
from .number import NumberOutput
from .rainbow import RainbowOutput
from .slider import SliderInput
from .touch import TouchInput
from .weather import WeatherInput

