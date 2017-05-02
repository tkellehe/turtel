This program takes the input and converts a string into a number and a number into a string. This can be used
to see what a number looks like in base96 (except the output will be modified) or see what the value of a
string is as a number.

       # Takes input implicitly and pushes it to the stack.
    ¦  # A NOOP because if the `¥` is the first character it will turn off auto popping.
     ¥ # Converts the top of the stack to a number if is a string and a string if is a number.
       # Implicitly pop the top of the stack and print to the screen.
