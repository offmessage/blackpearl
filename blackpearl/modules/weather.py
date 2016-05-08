from twisted.internet import defer

from .base import BaseModule


class Weather(BaseModule):
    
    module_name = 'weather'
    temperature = None
    pressure = None
    listening_for = ['weather']
    hardware_required = ['weather']
    
    def data(self, data):
        temp = data['temperature']
        if temp != self.temperature:
            self.temperature = temp
            self.temperature_changed(temp)
        pressure = data['pressure']
        if pressure != self.pressure:
            self.pressure = pressure
            self.pressure_changed(pressure)
            
    def temperature_changed(self, temp):
        pass
    
    def pressure_changed(self, pressure):
        pass
    
    
class WeatherRecorder(Weather):
    
    module_name = 'weather_recorder'
    freqency = 60 # Number of seconds between reports
    
    def setup(self):
        self.start()
        
    def update(self):
        data = {'temperature': self.temperature,
                'pressure': self.pressure,
                }
        self.emit(data)
        
    @defer.deferredGenerator
    def start(self):
        d = defer.Deferred()
        reactor.callLater(self.freqency, d.callback, self.update())
        wfd = defer.waitForDeferred(d)
        yield wfd
     
     
class TemperatureAlert(Weather):
    
    module_name = 'temperature_alert'
    above = None
    below = None
    status = 'ok'
    
    def setup(self):
        if self.above is not None and self.below is not None:
            if self.below >= self.above:
                raise ValueError("Cannot set the upper bound below the lower bound")
            
    def temperature_changed(self, temp):
        if self.above is not None and self.below is not None:
            if self.below < temp < self.above and self.status != 'ok':
                self.status = 'ok'
                data = {'status': self.status,
                        'temperature': self.temperature,
                        }
                self.emit(data)
                return
        if self.above is not None:
            if temp > self.above and self.status != 'ok':
                self.status = 'above'
                data = {'status': self.status,
                        'temperature': self.temperature,
                        }
                self.emit(data)
            elif temp <= self.above and self.status == 'above':
                self.status = 'ok'
                data = {'status': self.status,
                        'temperature': self.temperature,
                        }
                self.emit(data)
        if self.below is not None:
            if temp < self.below and self.status != 'ok':
                self.status = 'below'
                data = {'status': self.status,
                        'temperature': self.temperature,
                        }
                self.emit(data)
            elif temp >= self.below and self.status == 'below':
                self.status = 'ok'
                data = {'status': self.status,
                        'temperature': self.temperature,
                        }
                self.emit(data)
                

class PressureAlert(Weather):
    
    module_name = 'pressure_alert'
    above = None
    below = None
    status = 'ok'
    
    def setup(self):
        if self.above is not None and self.below is not None:
            if self.below >= self.above:
                raise ValueError("Cannot set the upper bound below the lower bound")
            
    def pressure_changed(self, pressure):
        if self.above is not None and self.below is not None:
            if self.below < pressure < self.above and self.status != 'ok':
                self.status = 'ok'
                data = {'status': self.status,
                        'pressure': self.pressure,
                        }
                self.emit(data)
                return
        if self.above is not None:
            if pressure > self.above and self.status != 'ok':
                self.status = 'above'
                data = {'status': self.status,
                        'pressure': self.pressure,
                        }
                self.emit(data)
            elif pressure <= self.above and self.status == 'above':
                self.status = 'ok'
                data = {'status': self.status,
                        'pressure': self.pressure,
                        }
                self.emit(data)
        if self.below is not None:
            if pressure < self.below and self.status != 'ok':
                self.status = 'below'
                data = {'status': self.status,
                        'pressure': self.pressure,
                        }
                self.emit(data)
            elif pressure >= self.below and self.status == 'below':
                self.status = 'ok'
                data = {'status': self.status,
                        'pressure': self.pressure,
                        }
                self.emit(data)
                
            