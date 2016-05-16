from .base import LinearInput


class Dial(LinearInput):
    """
    Dial
    ====
    
    NB: While the device is capable of returning between 0 and 1023 we limit
    the output to between 0 and 1000. In addition, anything below 6 gets
    returned as 0. The device was too inaccurate at the extremes of its inputs
    
    Outputs
    -------
    Emits a single integer
    
    Example:
    
    ``{'dial': {'value': 934}}``
    """
    module = "dial"
    

