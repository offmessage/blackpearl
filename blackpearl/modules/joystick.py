from .base import FlotillaInput

class JoystickInput(FlotillaInput):
    """
    The Joystick.
    """
    module = "joystick"
    COORDINATES = {x:0,
                   y:0,
                   }
    BUTTON = False
    
    def change(self, data):
        print(data)
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
        return {'coordinates': coordinates,
                'button': button,
                }
    

