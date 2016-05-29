from .base import FlotillaOutput


class Number(FlotillaOutput):
    """
    Number
    """
    module = "number"
    
    brightness = 40
    digits = [0, 0, 0, 0, ]
    colon = 0
    apostrophe = 0
    number = None
    hours = None
    minutes = None
    seconds = None
    
    def reset(self):
        self.brightness = 40
        self.digits = [0, 0, 0, 0,]
        self.colon = 0
        self.apostrophe = 0
        self.number = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.update()
    
    def set_digit(self, posn, digit):
        valid = [None, '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 '0.', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.',]
        if digit not in valid:
            raise ValueError("digit must be one of " + ", ".join(valid))
        
        if digit is None:
            value = 0
        elif digit == '-':
            value = NUM_MID
        elif len(digit) == 1:
            value = NUMBERS[int(digit)]
        else:
            value = NUMBERS[int(digit[0])]+1
        self.set_value(posn, value)
        
    def set_value(self, posn, value):
        if not (0 <= value <= 255):
            raise ValueError("value should be between 0 and 255")
        if not (0 <= posn <= 3):
            raise ValueError("posn should be between 0 and 3")
        self.digits[posn] = value
        
    def set_number(self, number, pad=None, precision=''):
        # XXX TODO: allow left right pad too, so that we can have 54.70
        print(number)
        if pad not in [None, '-', '0',]:
            raise ValueError("invalid pad character")
        if precision not in ['', '0', '00', '000']:
            raise ValueError("invalid precision, must be one of '', '0', '00' or '000'")
        if not (-999 <= number <= 9999):
            raise ValueError("Number is too large. Must be between -999 and 9999")
        
        self.number = number
        self.hours, self.minutes, self.seconds = None, None, None
        
        digits = list(str(number))
        
        # Need to calculate if we need to left pad, and what with
        count = len(digits)
        haspoint = False
        if "." in digits:
            # decimals don't consume a whole digit on the output
            count = count - 1
            haspoint = True
            # Now right pad with zeroes if we've been asked to
            units, decimals = str(number).split('.')
            if len(decimals) < len(precision):
                addn_zeroes = ['0',] * (len(precision) - len(decimals))
                digits.extend(addn_zeroes)
                count = len(digits) - 1
        if haspoint and count > 4:
            # we need to trim off extraneous decimal points
            digits = digits[:5]
            if digits[4] == '.':
                # case where we have a 4 digit number with a decimal point 
                # strip *all* decimals, including the point
                digits = digits[:4]
                haspoint = False
        for i in range(4 - count):
            # left pad with *pad* as appropriate
            digits.insert(0, pad)
        
        workingdigit = 0
        print(digits)
        for i in range(len(digits)):
            if not haspoint:
                # simple case, no decimal point
                self.set_digit(workingdigit, digits[i])
                workingdigit += 1
                continue
            
            # test if there is a decimal point at [i+1]
            if digits[i] == '.':
                continue
            if i == (len(digits) - 1):
                # we know this is the last digit and won't have a decimal point
                self.set_digit(workingdigit, digits[i])
            elif digits[i+1] == '.':
                self.set_digit(workingdigit, digits[i]+digits[i+1])
            else:
                self.set_digit(workingdigit, digits[i])
            workingdigit += 1
        
    def set_hoursminutes(self, hours, minutes, pad="0"):
        # XXX TODO This is no use, as seen by examples/clock.py
        # Needs refreshing to match actual use
        if pad not in [None, '0']:
            raise ValueError("invalid pad character")
        
        if not (0 <= hours <= 23):
            raise ValueError("Hours must be between 0 and 23")
        if not (0 <= minutes <= 59):
            raise ValueError("Minutes must be between 0 and 59")
        
        self.hours, self.minutes = hours, minutes
        self.number, self.seconds = None, None
        
        self.colon = 1
        
        hours = list(str(hours))
        if len(hours) == 1:
            hours.insert(0, pad)
            
        minutes = list(str(minutes))
        if len(minutes) == 1:
            minutes.insert(0, pad)
            
        digits = hours + minutes
        
        for i in range(4):
            self.set_digit(i, digits[i])
        
    def set_minutesseconds(self, minutes, seconds, pad=None):
        # XXX TODO This is no use, as seen by examples/clock.py
        # Needs refreshing to match actual use
        # Seconds always need padding, minutes padding is optional
        if pad not in [None, '0']:
            raise ValueError("invalid pad character")
        
        if not (0 <= minutes <= 59):
            raise ValueError("Minutes must be between 0 and 59")
        if not (0 <= seconds <= 59):
            raise ValueError("Seconds must be between 0 and 59")
        
        self.minutes, self.seconds = minutes, seconds
        self.number, self.hours = None, None

        self.colon = 1
        
        minutes = list(str(minutes))
        if len(minutes) == 1:
            minutes.insert(0, pad)
            
        seconds = list(str(seconds))
        if len(seconds) == 1:
            seconds.insert(0, pad)
            
        digits = minutes + seconds
        
        for i in range(4):
            self.set_digit(i, digits[i])
            
    def update(self):
        data = self.digits + [self.colon, self.apostrophe, self.brightness,]
        self.send(data)
        

NUM_DOT = 1
NUM_MID = 2
NUM_TL = 4
NUM_BL = 8
NUM_B = 16
NUM_BR = 32
NUM_TR = 64
NUM_T = 128

NUMBERS = [
    NUM_TL + NUM_BL + NUM_T + NUM_B + NUM_TR + NUM_BR,            # 0
    NUM_TR + NUM_BR,                                              # 1
    NUM_BL + NUM_T + NUM_B + NUM_TR + NUM_MID,                    # 2
    NUM_T + NUM_B + NUM_TR + NUM_BR + NUM_MID,                    # 3
    NUM_TR + NUM_TL + NUM_MID + NUM_BR,                           # 4
    NUM_TL + NUM_BR + NUM_MID + NUM_T + NUM_B,                    # 5
    NUM_T + NUM_MID + NUM_B + NUM_BL + NUM_BR + NUM_TL,           # 6
    NUM_T + NUM_TR + NUM_BR,                                      # 7
    NUM_TL + NUM_BL + NUM_T + NUM_B + NUM_TR + NUM_BR + NUM_MID,  # 8
    NUM_TL + NUM_T + NUM_TR + NUM_BR + NUM_MID                    # 9
    ]