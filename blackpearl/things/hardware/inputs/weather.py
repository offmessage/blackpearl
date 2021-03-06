from .base import FlotillaInput


class Weather(FlotillaInput):
    """
    Weather
    =======
    
    NB: Like the motion this is hypersensitive. Expect a lot of noise.
    
    Outputs
    -------
    Output is converted into Celsius and hPa (hectopascals/mbar) for more human
    readability. It broadcasts two floats - ``temperature`` and ``pressure``.
    
    Example::
    
      {'weather': {'temperature': 23.45,
                   'pressure': 1013.25,
                   }
       }
    """
    module = "weather"
    TEMPERATURE = None
    PRESSURE = None
    
    def change(self, data):
        temp, pressure = data.split(b',')
        temp = int(temp)/100.0 # Celsius
        pressure = int(pressure)/100.0 # hPa/mbar
        if self.TEMPERATURE == temp and self.PRESSURE == pressure:
            # This should never happen
            return None
        self.TEMPERATURE = temp
        self.PRESSURE = pressure
        output = {'temperature': temp,
                  'pressure': pressure,
                  }
        return self.broadcast(output)
