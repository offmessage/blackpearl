from .base import HardwareOutput


class Number(HardwareOutput):
    
    module_name = 'number'
    
    def reset(self):
        return self.module.reset()
    
    def set_digit(self, posn, digit):
        return self.module.set_digits(posn, digit)
    
    def set_number(self, number, pad=None):
        return self.module.set_number(number, pad)
        
    def set_hoursminutes(self, hours, minutes, pad="0"):
        return self.module.set_hoursminutes(hours, minutes, pad)
        
    def set_minutesseconds(self, minutes, seconds, pad=0):
        return self.module.set_minutesseconds(minutes, seconds, pad)

    
