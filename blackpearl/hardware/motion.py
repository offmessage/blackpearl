from .base import FlotillaInput

class MotionInput(FlotillaInput):
    """
    Motion sensor
    =============
    
    NB: This is hyper sensitive. Look at the recipes to see how to ignore some
    of the noise this generates.
    NB: The sensor returns 6 numbers, the Pimoroni Python API ignores the last
    3, so I do too...
    
    Outputs
    -------
    
    Returns a dictionary of coordinates x, y and z
    
    Example::
    
      {'motion': {'coordinates': {'x': 145,
                                  'y': 196,
                                  'z': 200,
                                  }
                  }
       }
    """
    # XXX TODO understand the bounds of how this one works
    module = "motion"
    COORDINATES = [0,0,0,]
    
    def change(self, data):
        x, y, z, i, j, k = data.split(b',')
        coordinates = [int(x), int(y), int(z),]
        if coordinates == self.COORDINATES:
            # This will happen frequently, as i, j and k change
            return None
        self.COORDINATES = coordinates
        output = {'x': coordinates[0],
                  'y': coordinates[1],
                  'z': coordinates[2],
                  }
        return self.broadcast({'coordinates': output})
    

