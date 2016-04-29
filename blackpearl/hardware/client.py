"""
==============
FlotillaClient
==============

This is the core Python code for connecting to, processing input from, and
sending messages to the Flotilla itself.

Each individual component can be found in hardware/
"""

import time

from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver

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


class FlotillaClient(LineReceiver):
    
    MODULES = {'matrix': MatrixOutput,
               'number': NumberOutput,
               'rainbow': RainbowOutput,
               'motor': MotorOutput,
               'touch': TouchInput,
               'dial': DialInput,
               'slider': SliderInput,
               'joystick': JoystickInput,
               'motion': MotionInput,
               'light': LightInput,
               'colour': ColourInput,
               'weather': WeatherInput,
               }
    
    def _resetModules(self):
        self.modules = { x: None for x in range(1, 9) }
        
    def run(self, project, reactor):
        self.project = project
        flotilla_port = self.project._flotilla_port
        baudrate = self.project._baudrate
        SerialPort(self, flotilla_port, reactor, baudrate)
        
    def connectionLost(self, reason):
        self._resetModules()
        print('Flotilla is disconnected.')
        
    def connectionMade(self):
        # XXX This needs far better error handling!
        self._resetModules()
        print('Flotilla is connected.')
        self.flotillaCommand(b'e')
        
    def flotillaCommand(self, cmd):
        self.delimiter = b'\r'
        self.sendLine(cmd)
        self.delimiter = b'\r\n'
        
    def handle_C(self, channel, module):
        print("Found a {} on channel {}".format(module, channel))
        new_module = self.MODULES[module](self, channel)
        self.modules[channel] = new_module
        # XXX This is shonky - needs to handle the race between module
        # XXX instantiation and the Flotilla waking up much better
        self.project.connect()
            
    def handle_D(self, channel, module):
        self.modules[channel] = None
        # XXX we should send a message to the project that a new module
        # has been deleted
        
    def handle_U(self, channel, module, data):
        if self.modules[channel] is None:
            # We appear to have a problem with the Flotilla here, where modules
            # are reporting data so quickly and frequently that the Flotilla
            # can't respond to a request to enumerate the connected modules.
            # We should probably emit an 'e' at this point?
            return
        j = self.modules[channel].change(data)
        
    def message(self, data):
        self.project.message(data)
        
    def connectedModules(self, type_=None):
        if type_ is None:
            return self.modules.values()
        return [ m for m in self.modules.values() if m is not None and m.module == type_ ]
    
    def firstOf(self, type_):
        modules = self.connectedModules(type_)
        if len(modules) == 0:
            return None
        l = [ (m.channel, m) for m in modules ]
        l.sort()
        return l[0][1]
        
    def lineReceived(self, line):
        # XXX: Needs better error handling
        parts = line.split(b" ")
        cmd = parts[0]
        if cmd == b'#':
            print(line)
            return
        channel, module = parts[1].decode('ascii').split('/')
        channel = int(channel)
        if cmd == b'c':
            self.handle_C(channel, module)
            return
        if cmd == b'd':
            self.handle_D(channel, module)
            return
        if cmd == b'u':
            data = parts[2]
            self.handle_U(channel, module, data)
            return

