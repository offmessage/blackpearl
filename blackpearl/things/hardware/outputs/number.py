from .base import FlotillaOutput


class Number(FlotillaOutput):
    """
    Number
    """
    module = "number"
    
    brightness = 40
    digits = [0, 0, 0, 0, ]
    colon = False
    apostrophe = False
    number = None
    hours = None
    minutes = None
    seconds = None
    
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
    
    def reset(self):
        self.brightness = 40
        self.digits = [0, 0, 0, 0,]
        self.colon = False
        self.apostrophe = False
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
            value = self.NUM_MID
        elif len(digit) == 1:
            value = self.NUMBERS[int(digit)]
        else:
            value = self.NUMBERS[int(digit[0])]+1
        self.set_value(posn, value)
        
    def set_value(self, posn, value):
        if not (0 <= value <= 255):
            raise ValueError("value should be between 0 and 255")
        if not (0 <= posn <= 3):
            raise ValueError("posn should be between 0 and 3")
        self.digits[posn] = value
        
    def set_number(self, number, pad=None, precision=''):
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
        
    def update(self):
        if self.colon:
            colon = 1
        else:
            colon = 0
        if self.apostrophe:
            apostrophe = 1
        else:
            apostrophe = 0
        data = self.digits + [colon, apostrophe, self.brightness,]
        self.send(data)
        

