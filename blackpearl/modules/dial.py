from .base import HardwareInput


class Dial(HardwareInput):
    
    module_name = 'dial'
    value = None
    
    def data(self, data):
        value = data['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    
    
