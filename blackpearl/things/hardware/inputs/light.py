from .base import FlotillaInput


class Light(FlotillaInput):
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
        visible = int(visible)
        infrared = int(infrared)
        lux = int(lux)
        if self.visible == visible and self.infrared == infrared and self.lux == lux:
            # This should never happen
            return None
        self.visible = visible
        self.infrared = infrared
        self.lux = lux
        data = {'visible': visible,
                'infrared': infrared,
                'lux': lux,
                }
        return self.broadcast(data)


