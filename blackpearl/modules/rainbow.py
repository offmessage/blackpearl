from itertools import chain

from twisted.internet import defer
from twisted.internet import reactor

from .base import FlotillaOutput

try:
    import blackpearl.wingdbstub
except ImportError:
    pass

class RainbowOutput(FlotillaOutput):
    """
    Matrix
    """
    module = "rainbow"
    
    #brightness = 150 # defined in the python API, but never sent
    pixels = [(0, 0, 0,),
              (0, 0, 0,),
              (0, 0, 0,),
              (0, 0, 0,),
              (0, 0, 0,),
              ]
    
    def reset(self):
        #self.brightness = 150 # defined in the python API, but never sent
        self.set_all(0, 0, 0)
        self.update()
    
    def update(self):
        data = list(chain.from_iterable([ list(pixel) for pixel in self.pixels ]))
        print(data)
        self.send(data)
        
    def set_pixel(self, pos, r, g, b):
        if pos > 4:
            raise TypeError
        if max([r,g,b]) > 255:
            raise TypeError
        if min([r,g,b]) < 0:
            raise TypeError
        self.pixels[pos] = (r, g, b)
    
    def set_all(self, r, g, b):
        if max([r,g,b]) > 255:
            raise TypeError
        if min([r,g,b]) < 0:
            raise TypeError
        for i in range(5):
            self.set_pixel(i, r, g, b)
            
    def hue(self, value):
        print(value)
        h = value
        s = 1.0
        v = 1.0
        
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        if i % 6 == 0:
            r = v
            g = t
            b = p
        elif i % 6 == 1:
            r = q
            g = v
            b = p
        elif i % 6 == 2:
            r = p
            g = v
            b = t
        elif i % 6 == 3:
            r = p
            g = q
            b = v
        elif i % 6 == 4:
            r = t
            g = p
            b = v
        elif i % 6 == 5:
            r = v
            g = p
            b = q
        rgb = [int(r*255), int(g*255), int(b*255)]
        print(rgb)
        return rgb
    