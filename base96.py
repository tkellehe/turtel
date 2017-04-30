# -*- coding: UTF-8 -*-
import characters

digits = characters.printables[:-1]
int_to_char = digits
char_to_int = dict()

for i in range(0, 96):
    char_to_int[int_to_char[i]] = int(i)

#########################################################################################
# Does not handle fixed point.
def whole_base10_to_base96(value):
    x = abs(int(value))
    if x == 0:
        return int_to_char[0]
    output = ""
    while x:
        output = int_to_char[x % 96] + output
        x = int(x / 96)
    return output

def whole_base96_to_base10(value):
    output = int(0)
    length = len(value)
    for i in range(0, length):
        output += char_to_int[value[length - i - 1]] * (96**i);
    return output

#########################################################################################
# Handles decimal numbers
def base10_to_base96(value):
    value = abs(value)
    whole = int(value)
    decimal = str(value - whole)[2:]
    return whole_base10_to_base96(whole) + ((characters.decimal + whole_base10_to_base96(int(decimal))) if len(decimal) and int(decimal) != 0 else "")

def base96_to_base10(value):
    parts = value.split(characters.decimal)
    if len(parts) == 1:
        return float(whole_base96_to_base10(parts[0]))
    if len(parts) == 2:
        return float(str(whole_base96_to_base10(parts[0])) + "." + str(whole_base96_to_base10(parts[1])))
    raise Exception("To many decimals to interpret into a base10 from a base96.")

#########################################################################################
# Returns true if lhs is smaller.
def whole_less_than(lhs, rhs):
    if len(lhs) > len(rhs):
        return False
    if len(lhs) < len(rhs):
        return True
    for i in range(0, len(lhs)):
        if char_to_int[lhs[i]] < char_to_int[rhs[i]]:
            return True
    return False

#########################################################################################
# Returns true if lhs is larger.
def whole_greater_than(lhs, rhs):
    if len(lhs) < len(rhs):
        return False
    if len(lhs) > len(rhs):
        return True
    for i in range(0, len(lhs)):
        if char_to_int[lhs[i]] > char_to_int[rhs[i]]:
            return True
    return False

#########################################################################################
# Adding whole numbers together.
add_table = []
for i in range(0, 96):
    add_table.append([])
    for j in range(0, 96):
        add_table[i].append((i+j > 95, int_to_char[(i+j)%96]))

def whole_add(lhs, rhs):
    if len(lhs) == 0 or lhs == "\n":
        return rhs
    if len(rhs) == 0 or rhs == "\n":
        return lhs
    if len(lhs) == 1 and len(rhs) == 1:
        carry, value = add_table[char_to_int[lhs]][char_to_int[rhs]]
        return (" " if carry else "") + value
    if len(lhs) < len(rhs):
        lhs = "{0:\n>{1}}".format(lhs, len(rhs))
    elif len(rhs) < len(lhs):
        rhs = "{0:\n>{1}}".format(rhs, len(lhs))
    output = ""
    i = len(lhs) - 1
    while i >= 0:
        carry, value = add_table[char_to_int[lhs[i]]][char_to_int[rhs[i]]]
        output = value + output
        if carry:
            lhs = whole_add(lhs, " " + ("\n" * (len(lhs) - i)))
            if len(lhs) > len(rhs):
                rhs = "{0:\n>{1}}".format(rhs, len(lhs))
                i += 1
        i -= 1
    return output

#########################################################################################
# Decimal addition.
def add(lhs, rhs):
    lhs = base96_to_base10(lhs)
    rhs = base96_to_base10(rhs)
    return base10_to_base96(lhs + rhs)

#########################################################################################
# Decimal subtraction.
def sub(lhs, rhs):
    lhs = base96_to_base10(lhs)
    rhs = base96_to_base10(rhs)
    return base10_to_base96(lhs - rhs)

#########################################################################################
# Decimal multiplication.
def multi(lhs, rhs):
    lhs = base96_to_base10(lhs)
    rhs = base96_to_base10(rhs)
    return base10_to_base96(lhs * rhs)

#########################################################################################
# Decimal division.
def div(lhs, rhs):
    lhs = base96_to_base10(lhs)
    rhs = base96_to_base10(rhs)
    return base10_to_base96(lhs / rhs)

#########################################################################################
# Decimal exponent.
def power(lhs, rhs):
    lhs = base96_to_base10(lhs)
    rhs = base96_to_base10(rhs)
    return base10_to_base96(lhs ** rhs)