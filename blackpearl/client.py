"""
==============
FlotillaClient
==============
"""


from twisted.protocols.basic import LineReceiver

from .modules.base import FlotillaOutput # temporary

from .modules import ColourInput
from .modules import DialInput
from .modules import JoystickInput
from .modules import LightInput
from .modules import MatrixOutput
from .modules import MotionInput
from .modules import SliderInput
from .modules import TouchInput
from .modules import WeatherInput


class FlotillaClient(LineReceiver):
    
    MODULES = {'matrix': MatrixOutput,
               'number': FlotillaOutput,
               'rainbow': FlotillaOutput,
               'motor': FlotillaOutput,
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
        self.modules = {0: None,
                        1: None,
                        2: None,
                        3: None,
                        4: None,
                        5: None,
                        6: None,
                        7: None,
                        }
        
    def connectionLost(self, reason):
        self._resetModules()
        print('Flotilla is disconnected.')
        
    def connectionMade(self):
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
        if module == 'matrix':
            self.modules[channel].scroll("Max is awesome and Amy isn't!")
        
    def handle_D(self, channel):
        self.modules[channel] = None
        
    def handle_U(self, channel, data):
        if self.modules[channel] is None:
            # We appear to have a problem with the Flotilla here, where modules
            # are reporting data so quickly and frequently that the Flotilla
            # can't respond to a request to enumerate the connected modules.
            return
        d = self.modules[channel].change(data)
        if d is not None:
            # here we loop through all the subscribers with the new data
            print(d)
        
    def connectedModules(self, type_=None):
        if type_ is None:
            return self.modules.values()
        return [ m for m in self.modules.values if m.module == type_ ]
    
    def firstOf(self, type_):
        modules = self.connectedModules(type_)
        if len(modules) == 0:
            return None
        l = [ (m.channel, m) for m in modules ]
        l.sort()
        return l[0][1]
        
    def lineReceived(self, line):      
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
            self.handle_D(channel)
            return
        if cmd == b'u':
            data = parts[2]
            self.handle_U(channel, data)
            return

