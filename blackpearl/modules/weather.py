from .base import HardwareInput


class Weather(HardwareInput):
    
    module_name = 'weather'
    temperature = None
    pressure = None
    
    def data(self, data):
        temp = data['temperature']
        if temp != self.temperature:
            self.temperature_changed(temp)
            self.temperature = temp
        pressure = data['pressure']
        if pressure != self.pressure:
            self.pressure_changed(pressure)
            self.pressure = pressure
            
    def temperature_changed(self, temp):
        pass
    
    def pressure_changed(self, pressure):
        pass
    
    
