"""
==============
FlotillaClient
==============
"""


import time

from twisted.protocols.basic import LineReceiver

from .modules import ColourInput
from .modules import DialInput
from .modules import JoystickInput
from .modules import LightInput
from .modules import MatrixOutput
from .modules import MotionInput
from .modules import MotorOutput
from .modules import NumberOutput
from .modules import RainbowOutput
from .modules import SliderInput
from .modules import TouchInput
from .modules import WeatherInput


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
            
    def handle_D(self, channel):
        self.modules[channel] = None
        
    def handle_U(self, channel, data):
        if self.modules[channel] is None:
            # We appear to have a problem with the Flotilla here, where modules
            # are reporting data so quickly and frequently that the Flotilla
            # can't respond to a request to enumerate the connected modules.
            # We should probably emit an 'e' at this point?
            return
        d = self.modules[channel].change(data)
        if d is not None:
            # here we loop through all the subscribers with the new data
            print(d)
            if 'buttons' in d:
                # It's a touch
                matrix = self.firstOf('matrix')
                #rainbow = self.firstOf('rainbow')
                motor = self.firstOf('motor')
                if d['buttons'][0]:
                    #rainbow.reset()
                    #rainbow.set_all(255,255,255)
                    #rainbow.update()
                    matrix.reset()
                    matrix.addColumn(127)
                    matrix.addColumn(1)
                    matrix.addColumn(3)
                    matrix.addColumn(7)
                    matrix.addColumn(15)
                    matrix.addColumn(31)
                    matrix.addColumn(63)
                    matrix.addColumn(127)
                    matrix.addFrame([255,255,255,255,255,255,255,255])
                    matrix.addText("1234567890")
                    matrix.scrollspeed = 2
                    matrix.loop = True
                    matrix.scroller()
                if d['buttons'][1]:
                    #rainbow.reset()
                    matrix.reset()
                    motor.stop()
                if d['buttons'][3]:
                    matrix.pause()
                if d['buttons'][2]:
                    #rainbow.set_all(255, 0, 0)
                    #rainbow.update()
                    motor.set_speed(50)
            if 'slider' in d:
                matrix = self.firstOf('matrix')
                if matrix is not None:
                    value = d['slider']
                    if 0 <= value < 200:
                        speed = 0.3
                    elif 200 <= value < 400:
                        speed = 0.2
                    elif 400 <= value < 600:
                        speed = 0.1
                    elif 600 <= value < 800:
                        speed = 0.07
                    else:
                        speed = 0.03
                    matrix.scrollspeed = speed
                rainbow = self.firstOf('rainbow')
                if rainbow is not None:
                    color = rainbow.hue(value/1000.0)
                    rainbow.set_all(*color)
                    rainbow.update()
                motor = self.firstOf('motor')
                if motor is not None:
                    motor.linearinput(value)
                
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
        # TODO:
        # Better error handling
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

