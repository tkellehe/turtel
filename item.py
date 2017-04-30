# -*- coding: utf-8 -*-
import characters
import base96
# For strings the `¶` should be used for positioning.

def itemize(item):
    if type(item) is list:
        raise Exception("Arrays are not supported.")
    elif item == None:
        return ITEM()
    return ITEM(item)

class ITEM:
    def __init__(self, value = ""):
        if type(value) is str:
            self.value = value
            self.to_string()
        elif type(value) is ITEM:
            self.value = value.value
            self.type = value.type
            self.is_string = value.is_string
            self.is_number = value.is_number
        else:
            self.value = base96.base10_to_base96(value)
            self.to_number()
    def to_string(self):
        self.type = "string"
        self.is_string = True
        self.is_number = False
    def to_number(self):
        self.type = "number"
        self.is_string = False
        self.is_number = True
    def printify(self):
        if self.is_string:
            return self.value.replace(characters.decimal, "")
        # For numbers the `¶` should be used as a decimal.
        elif self.is_number:
            s = str(base96.base96_to_base10(self.value))
            if s[-2:] == ".0":
                return s[:-2]
            return s
    def get_value(self):
        if self.is_string:
            return self.value.replace(characters.decimal, "")
        # For numbers the `¶` should be used as a decimal.
        elif self.is_number:
            return base96.base96_to_base10(self.value)
    def add(self, rhs):
        if self.is_string:
            if type(rhs) is ITEM:
                if rhs.is_string:
                    return ITEM(self.value + rhs.value)
                elif rhs.is_number:
                    return ITEM(self.value + str(base96.base96_to_base10(rhs.value)))
            else:
                return ITEM(self.value + str(rhs))
        elif self.is_number:
            if type(rhs) is ITEM:
                if rhs.is_string:
                    return ITEM(self.value + rhs.value)
                elif rhs.is_number:
                    return ITEM(base96.add(self.value, rhs.value))
            else:
                return ITEM(self.value + float(rhs))