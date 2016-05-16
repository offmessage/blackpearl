from .base import FlotillaInput

class LightInput(FlotillaInput):
    """
    Light sensor
    ============
    
    
    NB: Like the motion this is hypersensitive. Expect a lot of noise.
    
    Outputs
    -------
    Output is converted into Celsius and kPa (kilopascals) for more human
    readability. It broadcasts three integers - ``visible``, ``infrared`` and
    ``lux``. ``lux`` is probably the most useful. ``lux`` is constrained
    between 0 and 65536.
    
    https://gadgetoid.gitbooks.io/flotilla-protocol/content/light.html
    
    Example::
    
      {'light': {'visible': 136,
                 'infrared': 421,
                 'lux': 723,
                 }
       }
    """
    module = "light"
    visible = None
    infrared = None
    lux = None
    
    def change(self, data):
        visible, infrared, lux = data.split(b',')
        value = int(value)
        if self.VALUE == value:
            # This might happen due to dunno1 and dunno2 potentially changing
            return None
        self.VALUE = value
        return self.broadcast({'level': value,})


