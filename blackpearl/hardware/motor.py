from .base import FlotillaOutput


class MotorOutput(FlotillaOutput):
    """
    Motor
    Takes a speed between -63 and +63
    """
    module = "motor"
    
    #direction = 1
    speed = 0
    
    def stop(self):
        self.set_speed(0)
        
    def reset(self):
        self.set_speed(0)
    
    #def reverse(self):
        #self.direction = self.direction * -1
        #self.set_speed(self.speed * -1)
        
    #def set_direction(self, direction):
        #if direction in ["forwards", 1]:
            #self.direction = 1
        #elif direction in ["backwards", -1]:
            #self.direction = -1
        
    def update(self, data):
        data = [data,]
        self.send(data)
        
    def set_speed(self, v):
        # Let the user set the speed directly
        if max(v, 63) > 63:
            raise ValueError("Speed must be between -63 and +63. Speed was "+str(v))
        if min(v, -63) < -63:
            raise ValueError("Speed must be between -63 and +63. Speed was "+str(v))
        speed = int(v)
        self.update(speed)
        self.speed = speed
        
    #def linearinput(self, d):
        ## XXX TODO This should be factored into a recipe, not here
        ## d is between 0 and 1000 from our linear input modules
        #if d == 0:
            #v = -63
        #elif d == 1000:
            #v = 63
        #else:
            #v = int((d - 500)/8)
        #v = v * self.direction
        #self.set_speed(v)
        
