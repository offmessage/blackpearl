"""
==============
FlotillaClient
==============
"""

import json # This is temporary while we're still processing messages in here
import time

from twisted.protocols.basic import LineReceiver

from .hardware import ColourInput
from .hardware import DialInput
from .hardware import JoystickInput
from .hardware import LightInput
from .hardware import MatrixOutput
from .hardware import MotionInput
from .hardware import MotorOutput
from .hardware import NumberOutput
from .hardware import RainbowOutput
from .hardware import SliderInput
from .hardware import TouchInput
from .hardware import WeatherInput


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
        
    def connectionLost(self, reason):
        self._resetModules()
        self.subscribers = []
        print('Flotilla is disconnected.')
        
    def connectionMade(self):
        # XXX This needs far better error handling!
        self._resetModules()
        self.subscribers = []
        print('Flotilla is connected.')
        self.flotillaCommand(b'e')
        
    def flotillaCommand(self, cmd):
        self.delimiter = b'\r'
        self.sendLine(cmd)
        self.delimiter = b'\r\n'
        
    def addSubscriber(self, cls):
        self.subscribers.append(cls(self))
        
    def handle_C(self, channel, module):
        print("Found a {} on channel {}".format(module, channel))
        new_module = self.MODULES[module](self, channel)
        self.modules[channel] = new_module
        for s in self.subscribers:
            s.newModule(channel, module)
            
    def handle_D(self, channel, module):
        for s in self.subscribers:
            s.delModule(channel, module)
        self.modules[channel] = None
        
    def handle_U(self, channel, module, data):
        if self.modules[channel] is None:
            # We appear to have a problem with the Flotilla here, where modules
            # are reporting data so quickly and frequently that the Flotilla
            # can't respond to a request to enumerate the connected modules.
            # We should probably emit an 'e' at this point?
            return
        j = self.modules[channel].change(data)
        if j is None:
            return
        d = json.loads(j)
        for s in self.subscribers:
            # here we loop through all the subscribers with the new data
            s.update(channel, module, j)
        print(d)
        if 'touch' in d:
            # It's a touch
            matrix = self.firstOf('matrix')
            rainbow = self.firstOf('rainbow')
            motor = self.firstOf('motor')
            number = self.firstOf('number')
            if d['touch']['buttons']['1'] and matrix is not None:
                if rainbow is not None:
                    rainbow.reset()
                    rainbow.set_all(255,255,255)
                    rainbow.update()
                if matrix is not None:
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
                    matrix.frames()
            if d['touch']['buttons']['2']:
                if rainbow is not None:
                    rainbow.reset()
                if matrix is not None:
                    matrix.reset()
                if motor is not None:
                    motor.stop()
                if number is not None:
                    number.reset()
            if d['touch']['buttons']['3']:
                if rainbow is not None:
                    rainbow.set_all(255, 0, 0)
                    rainbow.update()
                if number is not None:
                    number.set_number(1223.2345)
                    number.update()
            if d['touch']['buttons']['4']:
                if matrix is not None:
                    matrix.pause()
        if 'slider' in d:
            value = d['slider']['value']
            rainbow = self.firstOf('rainbow')
            if rainbow is not None:
                color = rainbow.hue(value/1000.0)
                rainbow.set_all(*color)
                rainbow.update()
            motor = self.firstOf('motor')
            if motor is not None:
                motor.linearinput(value)
            number = self.firstOf('number')
            if number is not None:
                number.set_number(value, pad="0")
                number.update()
        if 'dial' in d:
            matrix = self.firstOf('matrix')
            if matrix is not None:
                value = d['dial']['value']
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
            self.handle_D(channel, module)
            return
        if cmd == b'u':
            data = parts[2]
            self.handle_U(channel, module, data)
            return

