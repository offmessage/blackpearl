from .base import FlotillaOutput

try:
    import blackpearl.wingdbstub
except ImportError:
    pass

class MotorOutput(FlotillaOutput):
    """
    Motor
    Takes a speed between -63 and +63
    """
    module = "motor"
    
    forwards = True
    
    def stop(self):
        self.update(0)
        
    def reset(self):
        self.set_speed(0)
        self.update()
    
    def reverse(self):
        self.forwards = not self.forwards
        
    def get_direction(self):
        if self.forwards:
            return "forwards"
        else:
            return "backwards"
    
    def set_direction(self, direction):
        if direction == "forwards":
            self.forwards = True
        elif direction == "backwards":
            self.forwards = False
        
    def update(self, data):
        data = [data,]
        self.send(data)
        
    def linearinput(self, d):
        # d is between 0 and 1000 from our linear input modules
        if self.forwards:
            mult = 1
        else:
            mult = -1
            
        if d == 0:
            v = -63
        elif d == 1000:
            v = 63
        else:
            v = int((d - 500)/8)
        v = v * mult
        self.set_speed(v)
        
    def set_speed(self, v):
        # Let the user set the speed directly
        if max(v, 63) > 63:
            raise TypeError("Speed must be between -63 and +63. Speed was "+str(v))
        if min(v, -63) < -63:
            raise TypeError("Speed must be between -63 and +63. Speed was "+str(v))
        speed = int(v)
        self.update(speed)