from itertools import chain

from .base import FlotillaOutput

try:
    import blackpearl.wingdbstub
except ImportError:
    pass

class RainbowOutput(FlotillaOutput):
    """
    Rainbow
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
        self.send(data)
        
    def set_pixel(self, posn, r, g, b):
        if posn > 4:
            raise ValueError("posn should be between 0 and 4")
        if max([r,g,b]) > 255:
            raise ValueError("r g & b should be less than 256")
        if min([r,g,b]) < 0:
            raise ValueError("r, g & b should be greater or equal than 0")
        self.pixels[posn] = (r, g, b)
    
    def set_all(self, r, g, b):
        if max([r,g,b]) > 255:
            raise ValueError("r, g & b should be less than 256")
        if min([r,g,b]) < 0:
            raise ValueError("r, g & b should be greater or equal than 0")
        for i in range(5):
            self.set_pixel(i, r, g, b)
            
    @staticmethod
    def hue(value):
        # XXX do some sense checking on input - we are everywhere else
        """
        This is wholesale lifted from the rockpool Javascript :)
        Takes a value between 0 and 1 and returns an RGB value
        """
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
        return rgb
    