from ..base import FlotillaInput


class Joystick(FlotillaInput):
    """
    Joystick
    ========
    
    Outputs
    -------
    Emits a complex dictionary, containing x and y coordinates and the state
    of the button. ``x`` and ``y`` are integers between ``0`` and ``1023``. The
    mid-point (Joystick resting) should be 512,512 (but in my case it's around
    468,487).
    
    ``button`` is boolean, ``True`` when pressed, ``False`` when released.
    
    Example::
    
      {'joystick': {'coordinates': {'x': 322,
                                    'y': 213,
                                    },
                    'button': True,
                    }
       }
    """
    module = "joystick"
    COORDINATES = {'x':0,
                   'y':0,
                   }
    BUTTON = False
    
    def change(self, data):
        button, x, y = data.split(b',')
        coordinates = {x: int(x),
                       y: int(y),
                       }
        button = bool(int(button))
        if coordinates == self.COORDINATES and button == self.BUTTON:
            # This should never happen
            return None
        self.COORDINATES = coordinates
        self.BUTTON = button
        output = {'coordinates': coordinates,
                  'button': button,
                  }
        return self.broadcast(output)
    

