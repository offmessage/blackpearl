from .base import FlotillaInput

class LightInput(FlotillaInput):
    """
    The Light sensor.
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
        return {'value': value,}


