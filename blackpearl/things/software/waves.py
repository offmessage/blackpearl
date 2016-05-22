import math

from .base import Timebased


class Wave(Timebased):
    
    tick_rate = 0.1
    frequency = 1
    min = 0
    max = 1
    startvalue = 0
    
    def __init__(self, module):
        super().__init__(module)
        self.amplitude = (self.max - self.min)/2
        

class Square(Wave):
    
    module = 'squarewave'
    
    def tick(self, tm):
        if not hasattr(self, '_current'):
            self._current = self.startvalue
        if tm % self.frequency == 0:
            if self._current == self.max:
                self._current = self.min
            else:
                self._current = self.max
        self.broadcast({'value': self._current})
        
        
class Sine(Wave):
    
    module = 'sinewave'
    min = -1
    max = 1
    
    def tick(self, tm):
        value = int((self.min + self.amplitude + (self.amplitude * math.sin(2*math.pi*self.frequency*tm)))*1000)/1000
        self.broadcast({'value': value})
        
    
class Triangle(Wave):
    
    module = 'trianglewave'
    
    def tick(self, tm):
        pass
    
    
class Saw(Wave):
    
    module = 'sawtoothwave'
    
    def tick(self, tm):
        pass
    
    
