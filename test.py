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

    fill_1 = Extendable()
    fill_1.x = turtles[current_turtle].pos[0]
    fill_1.y = turtles[current_turtle].pos[1]
    fill_1.width = 3
    fill_1.height = 7
    turtles[current_turtle].move = lambda x,y: move_fill(x,y,fill_1)
    turtles[current_turtle].write("012345678ABC")
    cout(printify(turtles))

    if len(stack):
        popped = stack.pop()
        turtles[current_turtle].write(popped.printify())

    cout(printify(turtles))


if __name__ == "__main__":
    main()
