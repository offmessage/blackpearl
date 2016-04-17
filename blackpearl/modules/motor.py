from .base import FlotillaOutput

try:
    import blackpearl.wingdbstub
except ImportError:
    pass

class MotorOutput(FlotillaOutput):
    """
    Motor
    """
    module = "motor"
    
    def stop(self):
        self.update(0)
        
    def reset(self):
        self.set_speed(0)
        self.update()
    
    def update(self, data):
        data = [data,]
        self.send(data)
        
    def linearinput(self, d):
        # d is between 0 and 1024
        if d == 0:
            v = -63
        elif d == 1024:
            v = 63
        else:
            v = int((d - 512)/8)
        self.set_speed(v)
        
    def set_speed(self, v):
        print("Speed:", v)
        if max(v, 63) > 63:
            raise TypeError("Speed must be between -63 and +63. Speed was "+str(v))
        if min(v, -63) < -63:
            raise TypeError("Speed must be between -63 and +63. Speed was "+str(v))
        speed = int(v)
        self.update(speed)