from .base import FlotillaInput

class MotionInput(FlotillaInput):
    """
    The Motion.
    TODO
     - we need to talk about sensitivity here
    """
    module = "motion"
    COORDINATES = [0,0,0,]
    
    def change(self, data):
        x, y, z = data.split(b',')
        coordinates = [int(x), int(y), int(z),]
        if coordinates == self.COORDINATES:
            # This should never happen
            return None
        self.COORDINATES = coordinates
        return {'coordinates': coordinates}
    

