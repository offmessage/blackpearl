from .base import HardwareOutput


class Number(HardwareOutput):
    
    module_name = 'number'
    
    def reset(self):
        return self.hardware.reset()
    
    def set_digit(self, posn, digit):
        return self.hardware.set_digits(posn, digit)
    
    def set_number(self, number, pad=None):
        return self.hardware.set_number(number, pad)
        
    def set_hoursminutes(self, hours, minutes, pad="0"):
        return self.hardware.set_hoursminutes(hours, minutes, pad)
        
    def set_minutesseconds(self, minutes, seconds, pad=0):
        return self.hardware.set_minutesseconds(minutes, seconds, pad)

    
