from .base import FlotillaInput


class Colour(FlotillaInput):
    """
    Colour
    ======
    
    https://gadgetoid.gitbooks.io/flotilla-protocol/content/colour.html
    
    Outputs
    -------
    Emits a list in traditional RGB form (e.g ``[r, g, b,]``) where all values
    are between 0 and 255 for rgb
    
    Example::
    
      {'colour': {'rgb': [82,72,157,],
                  'hex': '#52479d',
                  'raw': {'red': 441,
                          'green': 385,
                          'blue': 834,
                          'clear': 1361,
                          }
                  }
    """
    module = "colour"
    rgb = [0,0,0,]
    red = None
    green = None
    blue = None
    clear = None
    
    def change(self, data):
        red, green, blue, clear = data.split(b',')
        red = int(red)
        green = int(green)
        blue = int(blue)
        clear = int(clear)
        
        def convert(v):
            ratio = v/clear
            if ratio > 1:
                ratio = 1
                msg = ("Something went awry - was given a filtered light level"
                       "greater than the unfiltered light level.")
                self.flotilla.project.log("WARNING", msg)
            value = int(ratio * 255)
            return value
        
        rgb = [convert(red), convert(green), convert(blue),]
        
        print(rgb)
        
        if self.rgb == rgb:
            # This should never happen
            return None
        self.rgb = rgb
        hex_ = '#' + ''.join([ hex(v)[2:] for v in self.rgb ])
        self.red = red
        self.green = green
        self.blue = blue
        self.clear = clear
        output = {'rgb': rgb,
                  'hex': hex_,
                  'raw': {'red': red,
                          'green': green,
                          'blue': blue,
                          'clear': clear,
                          }
                  }
        return self.broadcast(output)
    
    
