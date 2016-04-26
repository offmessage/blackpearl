from .base import HardwareOutput


class Motor(HardwareOutput):
    
    module_name = 'motor'
    
    def stop(self):
        return self.hardware.stop()
        
    def reset(self):
        return self.hardware.reset()
    
    def reverse(self):
        return self.hardware.reverse()
        
    def set_direction(self, direction):
        return self.hardware.set_direction(direction)
        
    def set_speed(self, v):
        return self.hardware.set_speed(v)
        
    def linearinput(self, d):
        # XXX TODO Should this be factored into a special recipe, not here?
        # d is between 0 and 1000 from our linear input modules
        if d == 0:
            v = -63
        elif d == 1000:
            v = 63
        else:
            v = int((d - 500)/8)
        v = v * self.direction
        self.set_speed(v)

    
