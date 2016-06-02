from .base import Module
from ..things import Dial


class Dial(Module):
    
    listening_for = ['dial']
    hardware_required = [Dial,]
    
    module_name = 'dial_module' # icky, but it can't have the same name as the
                                # hardware itself
    value = None
    
    def receive(self, message):
        value = message['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    
    
