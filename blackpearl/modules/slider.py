from .base import Module
from ..things import Slider


class Slider(Module):
    
    listening_for = ['slider']
    hardware_required = [Slider,]

    module_name = 'slider_module' # icky, but it can't have the same name as the
                                  # hardware itself
    value = None

    def receive(self, message):
        value = message['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    

