from .base import FlotillaOutput


class Motor(FlotillaOutput):
    """
    Motor
    Takes a speed between -63 and +63
    """
    module = "motor"
    
    speed = 0
    
    def stop(self):
        self.set_speed(0)
        
    def reset(self):
        self.set_speed(0)
    
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
        
