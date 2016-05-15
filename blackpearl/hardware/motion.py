from .base import FlotillaInput

class MotionInput(FlotillaInput):
    """
    Motion sensor
    =============
    
    NB: This is hyper sensitive. Look at the recipes to see how to ignore some
    of the noise this generates.
    
    https://gadgetoid.gitbooks.io/flotilla-protocol/content/motion.html
    
    Outputs
    -------
    
    Returns a dictionary of coordinates x, y and z for both the accelerometer
    and the magnetometer.
    
    Example::
    
      {'motion': {'accelerometer': {'x': 145,
                                    'y': 196,
                                    'z': 200,
                                    },
                  'magnetometer': {'x': ,
                                   'y': ,
                                   'z': ,
                                   },
                  }
       }
    """
    module = "motion"
    accelerometer = [0,0,0,]
    magnetometer = [0,0,0,]
    
    def change(self, data):
        x, y, z, i, j, k = data.split(b',')
        accelerometer = [int(x), int(y), int(z),]
        magnetometer = [int(i), int(j), int(k),]
        
        if accelerometer == self.accelerometer and magnetometer = self.magnetometer:
            # This shouldn't happen
            return None
        self.accelerometer = accelerometer
        self.magnetometer = magnetometer
        output = {'accelerometer': {'x': accelerometer[0],
                                    'y': accelerometer[1],
                                    'z': accelerometer[2],
                                    },
                  'magnetometer': {'x': magnetometer[0],
                                   'y': magnetometer[1],
                                   'z': magnetometer[2],
                                   },
                  }
        return self.broadcast(output)
    

