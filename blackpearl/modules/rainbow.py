from .base import HardwareOutput


class Rainbow(HardwareOutput):
    
    module_name = 'rainbow'
    
    def reset(self):
        return self.hardware.reset()
    
    def set_pixel(self, posn, r, g, b):
        return self.hardware.set_pixel(posn, r, g, b)
    
    def set_all(self, r, g, b):
        return self.hardware.set_all(r, g, b)



