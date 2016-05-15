from .base import FlotillaInput

class ColourInput(FlotillaInput):
    """
    Colour
    ======
    
    NB: The Flotilla crew ignore the 'brightness' element (c), so I do too
    
    Outputs
    -------
    Emits a list in traditional RGB form (e.g ``[r, g, b,]``) where all values
    are between 0 and 255
    
    Example:
    
    ``{'colour': {'rgb': [255,255,255,]}}``
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
        return self.broadcast({'rgb': rgb})
    
    
