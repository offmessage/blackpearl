from collections import Counter

from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from blackpearl.client import FlotillaClient

class Recipe:
    
    def __init__(self):
        # Do lots of things
        # ...
        #
        flotilla = FlotillaClient()
        SerialPort(flotilla, '/dev/ttyACM0', reactor, baudrate=115200)
        reactor.run()
        
class BaseProject:
    
    def __init__(self, flotilla):
        self.flotilla = flotilla
        self._setModules()
        self._checkRequirements()
        
    def _setModules(self):
        """Create attributes on the instance for each connected module"""
        modules = self.flotilla.modules
        connected = {}
        for channel in modules:
            module = modules[channel]
            if module is not None:
                module_name = module.module
                connected.setdefault(module_name, 0)
                connected[module_name] += 1
                name = '{}{}'.format(module_name, connected[module_name])
                setattr(self, name, module)
                
    def _checkRequirements(self):
        """Subclasses will define a requirements attribute for connected
        modules. This is either a list: ['motor', 'motor', 'slider'], or a
        dict: {0: 'motor', 1: 'motor', 2: 'slider'}"""
        # XXX Check what numbering the channels are?
        if not hasattr(self, 'requirements'):
            # No requirements defined
            return
        
        if isinstance(self.requirements, list):
            reqs = Counter(self.requirements)
            mods = Counter(self.flotilla.modules.values())
            rem = mods - reqs
            if sum(rem.values()) == (sum(mods.values()) - sum(reqs.values())):
                # All our requirements are met
                return True
            print("Requirements not met")
            print("Requirements are:")
            for r in self.requirements:
                print("   "+r)
            print("Connected modules are:")
            for m in self.flotilla.modules:
                print("   {}: {}".format(m.channel, m.module))
            return False
        
        if isinstance(self.requirements, dict):
            for k in self.requirements:
                if self.requirements[k] != self.flotilla.modules[k]:
                    return
            print("Requirements not met")
            print("Requirements are:")
            for r in self.requirements:
                print("   {}: {}".format(r, self.requirements[r]))
            print("Connected modules are:")
            for m in self.flotilla.modules:
                print("   {}: {}".format(m.channel, m.module))
            return False
        
    def _addModule(self, channel, module):
        self._checkRequirements()
    
    def _delModule(self, channel, module):
        self._checkRequirements()
    
    def update(self, channel, module, data):
        pass
    
    
class TouchScroller(BaseProcessor):
    
    requirements = ['matrix', 'touch',]
    
    """when touch.button4 is pressed
    matrix.pause()
    when touch.button4 is released
    do nothing
    
    when touch.button1 is pressed
    add some text to the matrix
    matrix.scroll()"""
    
class Input:
    
    module_name = None
    
    def __init__(self, project, module):
        self.project = project
        self.module
        
    def dispatch(self, data):
        if self.module_name not in data:
            return
        self.data(data)
        
    def data(self, data):
        pass
    
        
class Colour(Input):
    pass


class Dial(Input):
    
    module_name = 'dial'
    value = None
    
    def data(self, data):
        value = data['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    
    
class Joystick(Input):
    pass


class Motion(Input):
    pass


class Slider(Input):
    
    module_name = 'slider'
    value = None
    
    def data(self, data):
        value = data['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    

class Touch(Input):
    
    module_name = 'touch'
    buttons = {1: False,
                2: False,
                3: False,
                4: False,
                }

    def data(self, data):
        buttons = data['buttons']
        for k in buttons:
            method_name = None
            if not self.buttons[k] and buttons[k]:
                # Button k has been pressed
                method_name = 'button{}_pressed'.format(k)
            if self.buttons[k] and not buttons[k]:
                # Button k has been released
                method_name = 'button{}_released'.format(k)
            if method_name is not None:
                method = getattr(self, method_name, None)
                if method is not None:
                    method()
                    
    def button1_pressed(self):
        pass
    
    def button1_released(self):
        pass
    
    def button2_pressed(self):
        pass
    
    def button2_released(self):
        pass
    
    def button3_pressed(self):
        pass
    
    def button3_released(self):
        pass
    
    def button4_pressed(self):
        pass
    
    def button4_released(self):
        pass
    

class Weather(Input):
    
    module_name = 'weather'
    temperature = None
    pressure = None
    
    def data(self, data):
        temp = data['temperature']
        if temp != self.temperature:
            self.temperature_changed(temp)
            self.temperature = temp
        pressure = data['pressure']
        if pressure != self.pressure:
            self.pressure_changed(pressure)
            self.pressure = pressure
            
    def temperature_changed(self, temp):
        pass
    
    def pressure_changed(self, pressure):
        pass
    
    
class Output:
    
    module_name = None
    
    def __init__(self, project, module):
        self.project = project
        self.module = module
        self.channel = module.channel
        
class Matrix(Output):
    
    module_name = 'matrix'
    
    def reset(self):
        return self.module.reset()
    
    def addText(self, text):
        return self.module.addText(text)
            
    def addColumn(self, column):
        """Bottom is 1, top is 128, we expect it bottom to top"""
        return self.module.addColumn(column)
        
    def addFrame(self, frame):
        """left to right"""
        return self.module.addFrame(frame)
        
    def next_frame(self):
        return self.module.next_frame()
        
    def frames(self):
        return self.scroller(steps=8)
        
    def scroll(self):
        return self.scroller(steps=1)
        
    def scroller(self, steps=1):
        return self.module.scroller(steps)
    
    def pause(self):
        return self.module.pause()
    
    
class Motor(Output):
    
    module_name = 'motor'
    
    def stop(self):
        return self.module.stop()
        
    def reset(self):
        return self.module.reset()
    
    def reverse(self):
        return self.module.reverse()
        
    def set_direction(self, direction):
        return self.module.set_direction(direction)
        
    def set_speed(self, v):
        return self.module.set_speed(v)
        
    def linearinput(self, d):
        # XXX TODO Should this be factored into a special recipe, not here?
        # d is between 0 and 1000 from our linear input modules
        if d == 0:
            v = -63
        elif d == 1000:
            v = 63
        else:
            v = int((d - 500)/8)
        v = v * self.direction
        self.set_speed(v)

    
class Number(Output):
    
    module_name = 'number'
    
    def reset(self):
        return self.module.reset()
    
    def set_digit(self, posn, digit):
        return self.module.set_digits(posn, digit)
    
    def set_number(self, number, pad=None):
        return self.module.set_number(number, pad)
        
    def set_hoursminutes(self, hours, minutes, pad="0"):
        return self.module.set_hoursminutes(hours, minutes, pad)
        
    def set_minutesseconds(self, minutes, seconds, pad=0):
        return self.module.set_minutesseconds(minutes, seconds, pad)

    
class Rainbow(Output):
    
    module_name = 'rainbow'
    
    def reset(self):
        return self.module.reset()
    
    def set_pixel(self, posn, r, g, b):
        return self.module.set_pixel(posn, r, g, b)
    
    def set_all(self, r, g, b):
        return self.module.set_all(r, g, b)
