from .base import HardwareOutput


class Rainbow(HardwareOutput):
    
    module_name = 'rainbow'
    
    def reset(self):
        return self.module.reset()
    
    def set_pixel(self, posn, r, g, b):
        return self.module.set_pixel(posn, r, g, b)
    
    def set_all(self, r, g, b):
        return self.module.set_all(r, g, b)



