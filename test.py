# -*- coding: UTF-8 -*-


from item import *
from turtle import *

import sys
import math

Extendable = type('Extendable', (object,), {})

def main():
    args = []
    if len(sys.argv) > 1:
        args.extend(eval(sys.argv[1]))
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

    stack.append(ITEM("A"))
    # NOOP
    stack.append(ITEM("B"))
    # NOOP
    stack.append(ITEM("C"))
    if len(stack) > 1:
        popped = stack.pop()
        while len(stack):
            popped.add_to(stack.pop())
        stack.push(popped)

    if implicit_pop_to_display and len(stack):
        popped = stack.pop()
        turtles[current_turtle].write(popped.printify())
    cout(printify(turtles))


if __name__ == "__main__":
    main()
