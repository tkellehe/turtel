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
    current_turtle = 0
    cout(printify(turtles))

    turtles[current_turtle].write("Loading... ")
    cout(printify(turtles))
    stack.append(ITEM('\\'))
    stack.append(ITEM('-'))
    stack.append(ITEM('/'))
    stack.append(ITEM('|'))
    while True:
        
        if len(stack) > 0:
            pos = turtles[current_turtle].pos
            turtles[current_turtle].write(stack[len(stack)-1].printify())
            turtles[current_turtle].pos = pos
        elif len(B):
            stack.append(B[len(B)-1])
            pos = turtles[current_turtle].pos
            turtles[current_turtle].write(stack[0].printify())
            turtles[current_turtle].pos = pos
        cout(printify(turtles))
        if len(stack):
            stack.insert(0, stack.pop())
        wait(250)

    if len(stack):
        popped = stack.pop()
        turtles[current_turtle].write(popped.printify())

    cout(printify(turtles))


if __name__ == "__main__":
    main()
