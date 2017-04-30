# -*- coding: UTF-8 -*-


from item import *
from turtle import *

import sys
import math

Extendable = type('Extendable', (object,), {})

def main():
    args = []
    args.extend(sys.argv[1:])
    for arg in range(0, len(args)):
        args[arg] = itemize(args[arg])
    stack = []
    for arg in args:
        stack.append(ITEM(arg))
    A = []
    B = []
    turtles = [Turtle()]
    implicit_pop_to_display = True
    current_turtle = 0
    cout(printify(turtles))

    stack.append(ITEM("abc"))
    # NOOP
    stack.append(ITEM("def"))
    if len(stack):
        A.append(stack.pop())
    if len(stack):
        if stack[len(stack)-1].is_number:
            stack[len(stack)-1].to_string()
        elif stack[len(stack)-1].is_string:
            stack[len(stack)-1].to_number()

    if implicit_pop_to_display and len(stack):
        popped = stack.pop()
        turtles[current_turtle].write(popped.printify())
    cout(printify(turtles))


if __name__ == "__main__":
    main()
