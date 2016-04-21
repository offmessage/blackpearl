from .base import FlotillaInput

class LightInput(FlotillaInput):
    """
    Light sensor
    ============
    
    NB: This returns 3 values, and no code I've found can tell me what the
    second and third are! I currently ignore them.
    
    Outputs
    -------
    Emits a single integer. Upper bound is very high. Normal room light levels
    are generally less than 1,000, but held close to a bright source the return
    value can be in the tens of thousands.
    
    Example:
    
    ``{'light': {'level': 672}}``
    """
    module = "light"
    VALUE = None
    
    def change(self, data):
        print(data)
        value, dunno1, dunno2 = data.split(b',')
        value = int(value)
        if self.VALUE == value:
            # This might happen due to dunno1 and dunno2 potentially changing
            return None
        self.VALUE = value
        return self.emit({'level': value,})


