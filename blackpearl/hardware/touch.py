from .base import FlotillaInput


class Touch(FlotillaInput):
    """
    Touch
    =====
    
    NB: Bizarrely it sends *n* on/off events for button *n* (so 4 for button 4,
    but only 1 for button 1).
    
    Outputs
    -------
    
    Emits a dictionary keyed on button number, with boolean values for each
    button on every change. Expect one event for press, and one for release.
    
    Example::
    
      {'touch': {'buttons': {'1': True,
                             '2': False,
                             '3': True,
                             '4': False,
                             }
                 }
       }
    """
    module = "touch"
    BUTTONS = [False, False, False, False,]
    
    def change(self, data):
        buttons = [ bool(int(b)) for b in data.split(b',') ]
        if self.BUTTONS == buttons:
            return None
        self.BUTTONS = buttons
        output = {'buttons': {'1': buttons[0],
                              '2': buttons[1],
                              '3': buttons[2],
                              '4': buttons[3],
                              }
                  }
        return self.broadcast(output)
        

