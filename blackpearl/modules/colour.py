from .base import FlotillaInput

class ColourInput(FlotillaInput):
    """
    Colour
    Notably the Flotilla crew ignore the 'brightness' element (c)!
    """
    module = "colour"
    RGB = [0,0,0,]
    
    def change(self, data):
        r, g, b, c = data.split(b',')
        rgb = [int(r), int(g), int(b),]
        if self.RGB == rgb:
            # This could happen, due to 'c' changing
            return None
        self.RGB = rgb
        return {'rgb': rgb}
    
    
