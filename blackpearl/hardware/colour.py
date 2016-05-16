from .base import FlotillaInput

class ColourInput(FlotillaInput):
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
            # The fact that we have to put this min() in there is a bit
            # worrying - I think my personal colour sensor may be over reporting
            # the levels of blue, as it's often *greater* than the value
            # reported from the unfiltered light sensor
            
            ratio = v/clear
            value = int(ratio * 255)
            if value > 255:
                print("Something went awry - was given a filtered light level"
                      "greater than the unfiltered light level")
                return 255
            return value
        rgb = [convert(red), convert(green), convert(blue),]
        
        print(rgb)
        
        if self.rgb == rgb:
            # This should never happen
            return None
        self.rgb = rgb
        self.red = red
        self.green = green
        self.blue = blue
        self.clear = clear
        output = {'rgb': rgb,
                  'raw': {'red': red,
                          'green': green,
                          'blue': blue,
                          'clear': clear,
                          }
                  }
        return self.broadcast(output)
    
    
