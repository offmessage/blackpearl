from .base import FlotillaInput

class WeatherInput(FlotillaInput):
    """
    Weather
    We need to talk about sensitivity here too
    """
    module = "weather"
    TEMPERATURE = None
    PRESSURE = None
    
    def change(self, data):
        temp, pressure = data.split(b',')
        temp = int(temp)/100.0 # Celsius
        pressure = int(pressure)/1000.0 # kPa
        if self.TEMPERATURE == temp and self.PRESSURE == pressure:
            # This should never happen
            return None
        self.TEMPERATURE = temp
        self.PRESSURE = pressure
        return {'temperature': temp,
                'pressure': pressure,
                }
