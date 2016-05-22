import math

from .base import Timebased


class Wave(Timebased):
    
    tick_rate = 0.1
    frequency = 1
    hi = 1
    lo = -1
    startvalue = 0
    
    def __init__(self, module):
        super().__init__(module)
        self.amplitude = self.hi - self.lo
        

class Square(Wave):
    
    module = 'squarewave'
    
    def tick(self, tm):
        if not hasattr(self, '_current'):
            self._current = self.startvalue
        if tm % self.frequency == 0:
            if self._current == self.hi:
                self._current = self.lo
            else:
                self._current = self.hi
        self.broadcast({'value': self._current})
        
        
class Sine(Wave):
    """https://en.wikipedia.org/wiki/Sine_wave"""
    
    module = 'sinewave'
    
    def __init__(self, module):
        super().__init__(module)
        self.amplitude = (self.hi - self.lo)/2
        
    def tick(self, tm):
        a = self.amplitude
        p = self.frequency
        pi = math.pi
        
        raw = a*math.sin(2*pi*p*tm)
        rounded = int(raw*1000)/1000
        shifted = self.lo + a + rounded
        self.broadcast({'value': shifted})
        
    
class Triangle(Wave):
    """https://en.wikipedia.org/wiki/Triangle_wave"""
    
    module = 'trianglewave'
    
    def tick(self, tm):
        a = self.amplitude
        p = self.frequency
        raw = (2*a/p)*(abs((tm % p) - p/2) - p/4)
        rounded = int(raw*1000)/1000
        shifted = self.lo + a/2 + rounded
        self.broadcast({'value': shifted})
    
    
class Sawtooth(Wave):
    """https://en.wikipedia.org/wiki/Sawtooth_wave"""
    
    module = 'sawtoothwave'
    
    def tick(self, tm):
        a = self.amplitude
        p = self.frequency
        raw = 2*((tm/p)-math.floor(1/2 + tm/p))
        # raw is of amplitude 2 (between -1 and 1) so shift it
        mult = raw * a/2
        rounded = int(mult*1000)/1000
        shifted = self.lo + a/2 + rounded
        self.broadcast({'value': shifted})
    
    
