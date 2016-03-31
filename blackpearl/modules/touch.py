from .base import FlotillaInput

class TouchInput(FlotillaInput):
    """
    The Touch.
    Bizarrely it sends *n* on/off events for button *n* (so 4 for button 4, but
    only 1 for button 1).
    """
    module = "touch"
    BUTTONS = [False, False, False, False,]
    
    def change(self, data):
        buttons = [ bool(int(b)) for b in data.split(b',') ]
        if self.BUTTONS == buttons:
            return None
        self.BUTTONS = buttons
        return {'buttons': buttons,}
        

