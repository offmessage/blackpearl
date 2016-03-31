"""
==============
FlotillaClient
==============
"""


from twisted.protocols.basic import LineReceiver


from modules.base import FlotillaOutput # temporary

from .modules import ColourInput
from .modules import DialInput
from .modules import JoystickInput
from .modules import LightInput
from .modules import MotionInput
from .modules import SliderInput
from .modules import TouchInput
from .modules import WeatherInput


class FlotillaClient(LineReceiver):
    
    MODULES = {'matrix': FlotillaOutput,
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
        self.modules[int(channel)] = new_module
        
    def handle_D(self, channel):
        self.modules[int(channel)] = None
        
    def handle_U(self, channel, data):
        if self.modules[int(channel)] is not None:
            # We appear to get a race condition here, where modules are
            # reporting data before they've been enumerated. This is a perfect
            # moment for callbacks, surely?
            d = self.modules[int(channel)].change(data)
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
        
    def lineReceived(self,data):      
        parts = line.split(b" ")
        cmd = parts[0]
        if cmd == b'#':
            print(line)
            return
        channel, module = parts[1].decode('ascii').split('/')
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

