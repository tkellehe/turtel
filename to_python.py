# -*- coding: UTF-8 -*-
import interpreter
import turtle
import base96

header = """# -*- coding: UTF-8 -*-

"""

starter = """
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

"""
implicit_pop_to_display_code = """
    if len(stack):
        popped = stack.pop()
        turtles[current_turtle].write(popped.printify())
"""
footer = """
    cout(printify(turtles))
"""

INDENT = "    "

script = interpreter.Script()

def translate(code):
    script.props.indent = 1
    script.props.identifier = 1
    script.props.implicit_pop_to_display = True
    script.parse(code)
    output = header
    # with open("item.py", "r") as file_py:
    #     output += file_py.read()
    #     output += "\n\n"
    # with open("turtle.py", "r") as file_py:
    #     output += file_py.read()
    #     output += "\n\n"
    output += starter
    for tkn in script.tokens:
        for line in tkn.props.tops:
            if type(line) is str:
                output += (INDENT*script.props.indent) + line + "\n"
            else:
                script.props.indent += line[0]
                if script.props.indent < 1:
                    script.props.indent = 1
                output += (INDENT*script.props.indent) + line[1] + "\n"

    script.props.indent = 1
    for tkn in script.tokens:
        for line in tkn.props.firsts:
            if type(line) is str:
                output += (INDENT*script.props.indent) + line + "\n"
            else:
                script.props.indent += line[0]
                if script.props.indent < 1:
                    script.props.indent = 1
                output += (INDENT*script.props.indent) + line[1] + "\n"
        for line in tkn.props.lines:
            if type(line) is str:
                output += (INDENT*script.props.indent) + line + "\n"
            else:
                script.props.indent += line[0]
                if script.props.indent < 1:
                    script.props.indent = 1
                output += (INDENT*script.props.indent) + line[1] + "\n"
        for line in tkn.props.lasts:
            if type(line) is str:
                output += (INDENT*script.props.indent) + line + "\n"
            else:
                script.props.indent += line[0]
                if script.props.indent < 1:
                    script.props.indent = 1
                output += (INDENT*script.props.indent) + line[1] + "\n"

    script.props.indent = 1
    for tkn in script.tokens:
        for line in tkn.props.bottoms:
            if type(line) is str:
                output += (INDENT*script.props.indent) + line + "\n"
            else:
                script.props.indent += line[0]
                if script.props.indent < 1:
                    script.props.indent = 1
                output += (INDENT*script.props.indent) + line[1] + "\n"

    if script.props.implicit_pop_to_display:
        output += implicit_pop_to_display_code
    output += footer

    output += """

if __name__ == "__main__":
    main()
"""
    script.tokens = []

    return output

def tokenize_basics(tkn):
    tkn.props.tops = []
    tkn.props.firsts = []
    tkn.props.lines = []
    tkn.props.lasts = []
    tkn.props.bottoms = []
    tkn.props.is_print_tkn = False

#########################################################################################
# String literals.
import characters
import re
def tokenize(tkn):
    def translator(tkn):
        string = ""
        if "string1" in tkn.symbols:
            string = tkn.symbols["string1"].value
        elif "string2" in tkn.symbols:
            string = tkn.symbols["string2"].value
        if string.count(u'¶') == 1:
            tkn.props.lines.append("stack.append(ITEM(\"" + characters.escape(string) + "\").to_number())")
        else:
            tkn.props.lines.append("stack.append(ITEM(\"" + characters.escape(string) + "\"))")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u"(?P<literal>(?:(?P<open1>“)(?P<string1>[" + re.escape(characters.printables) + u"]*)(?P<close1>”?))|(?:(?P<open2>“?)(?P<string2>[" + re.escape(characters.printables) + u"]*)(?P<close2>”)))"),
    0, tokenize))


#########################################################################################
# Commands for interfacing from stack to variable stacks.
def tokenize(tkn):
    def translator(tkn):
        cmd = int(characters.tiny_to_digit(tkn.literal.value))
        if cmd == 0:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    A.append(stack.pop())")
        elif cmd == 1:
            tkn.props.lines.append("if len(A):")
            tkn.props.lines.append("    stack.append(A.pop())")
            tkn.props.lines.append("else:")
            tkn.props.lines.append("    stack.reverse()")
        elif cmd == 2:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    A.append(ITEM(stack[len(stack)-1]))")
        elif cmd == 3:
            tkn.props.lines.append("if len(A):")
            tkn.props.lines.append("    stack.append(ITEM(A[len(A)-1]))")
            tkn.props.lines.append("else:")
            tkn.props.lines.append("    A.extend(stack)")
            tkn.props.lines.append("    # Looped through to keep the same list object.")
            tkn.props.lines.append("    while len(stack):")
            tkn.props.lines.append("        stack.pop()")
        elif cmd == 4:
            tkn.props.lines.append("if len(A):")
            tkn.props.lines.append("    stack.append(A[len(A)-1])")
            tkn.props.lines.append("elif len(stack):")
            tkn.props.lines.append("    A.append(stack[len(stack)-1])")
        elif cmd == 5:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    B.append(stack.pop())")
        elif cmd == 6:
            tkn.props.lines.append("if len(B):")
            tkn.props.lines.append("    stack.append(B.pop())")
            tkn.props.lines.append("else:")
            tkn.props.lines.append("    stack.reverse()")
        elif cmd == 7:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    B.append(ITEM(stack[len(stack)-1]))")
        elif cmd == 8:
            tkn.props.lines.append("if len(B):")
            tkn.props.lines.append("    stack.append(ITEM(B[len(B)-1]))")
            tkn.props.lines.append("else:")
            tkn.props.lines.append("    B.extend(stack)")
            tkn.props.lines.append("    # Looped through to keep the same list object.")
            tkn.props.lines.append("    while len(stack):")
            tkn.props.lines.append("        stack.pop()")
        elif cmd == 9:
            tkn.props.lines.append("if len(B):")
            tkn.props.lines.append("    stack.append(B[len(B)-1])")
            tkn.props.lines.append("elif len(stack):")
            tkn.props.lines.append("    B.append(stack[len(stack)-1])")


    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX("(?P<literal>[" + re.escape(characters.variables) + "])"),
    0, tokenize))


#########################################################################################
# If the first character it will turn off auto popping else will change
# between number and string.
def tokenize(tkn):
    def translator(tkn):
        if tkn.index == 0:
            tkn.snippet.script.props.implicit_pop_to_display = False
        else:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    if stack[len(stack)-1].is_number:")
            tkn.props.lines.append("        stack[len(stack)-1].to_string()")
            tkn.props.lines.append("    elif stack[len(stack)-1].is_string:")
            tkn.props.lines.append("        stack[len(stack)-1].to_number()")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX("(?P<literal>¥)"),
    0, tokenize))

#########################################################################################
# Wait for specified time.
map_wait_times = dict()
map_wait_times["s"] = "1000"
map_wait_times["h"] = "500"
map_wait_times["q"] = "250"
map_wait_times["e"] = "125"
map_wait_times["t"] = "100"
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) > 0 and len(tkn.params[0].value) > 0:
            tkn.props.lines.append("wait(" + map_wait_times[tkn.params[0].value] + ")")
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    wait(stack.pop().to_number().get_value())")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ẉ)([shqet]?)'),
    0, tokenize))

#########################################################################################
# Wait for specified time before running all the tokens that print.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) > 0 and len(tkn.params[0].value) > 0:
            for i in range(tkn.index+1, len(tkn.snippet.script.tokens)):
                if tkn.snippet.script.tokens[i].props.is_print_tkn:
                    tkn.snippet.script.tokens[i].props.lasts.append("wait(" + map_wait_times[tkn.params[0].value] + ")")
        else:
            for i in range(tkn.index+1, len(tkn.snippet.script.tokens)):
                if tkn.snippet.script.tokens[i].props.is_print_tkn:
                    tkn.snippet.script.tokens[i].props.lasts.append("if len(stack) > 0:")
                    tkn.snippet.script.tokens[i].props.lasts.append("    wait(stack.pop().to_number().get_value())")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>Ẉ)([shqet]?)'),
    0, tokenize))

#########################################################################################
# Most basic print that consumes from the current stack.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) and len(tkn.params[0].value):
            tkn.props.lines.append("turtles[current_turtle].write(\"" + characters.escape(tkn.params[0].value) + "\")")
        else:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    turtles[current_turtle].write(stack.pop().printify())")
            tkn.props.lines.append("elif len(A):")
            tkn.props.lines.append("    stack.append(A[len(A)-1])")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[0].printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>Þ)'),
    0, tokenize))

#########################################################################################
# Most basic print that does not consume from the current stack.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) and len(tkn.params[0].value):
            tkn.props.lines.append("turtles[current_turtle].write(\"" + characters.escape(tkn.params[0].value) + "\")")
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[len(stack)-1].printify())")
            tkn.props.lines.append("elif len(B):")
            tkn.props.lines.append("    stack.append(B[len(B)-1])")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[0].printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>þ)'),
    0, tokenize))

#########################################################################################
# Clears the current turtle then consumes from the current stack to the screen.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("turtles[current_turtle].clear()")
        if len(tkn.params) and len(tkn.params[0].value):
            tkn.props.lines.append("turtles[current_turtle].write(\"" + characters.escape(tkn.params[0].value) + "\")")
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    turtles[current_turtle].write(stack.pop().printify())")
            tkn.props.lines.append("elif len(A):")
            tkn.props.lines.append("    stack.append(A[len(A)-1])")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[0].printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>Ç)'),
    0, tokenize))

#########################################################################################
# Clears the current turtle then does not consume from the current stack to the screen.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("turtles[current_turtle].clear()")
        if len(tkn.params) and len(tkn.params[0].value):
            tkn.props.lines.append("turtles[current_turtle].write(\"" + characters.escape(tkn.params[0].value) + "\")")
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[len(stack)-1].printify())")
            tkn.props.lines.append("elif len(B):")
            tkn.props.lines.append("    stack.append(B[len(B)-1])")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[0].printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>ç)'),
    0, tokenize))

#########################################################################################
# Prints to the screen and resets the cursor.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) and len(tkn.params[0].value):
            tkn.props.lines.append("turtles[current_turtle].clear()")
            tkn.props.lines.append("pos = turtles[current_turtle].pos")
            tkn.props.lines.append("turtles[current_turtle].write(\"" + characters.escape(tkn.params[0].value) + "\")")
            tkn.props.lines.append("turtles[current_turtle].pos = pos")
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    pos = turtles[current_turtle].pos")
            tkn.props.lines.append("    turtles[current_turtle].write(stack.pop().printify())")
            tkn.props.lines.append("    turtles[current_turtle].pos = pos")
            tkn.props.lines.append("elif len(A):")
            tkn.props.lines.append("    stack.append(A[len(A)-1])")
            tkn.props.lines.append("    pos = turtles[current_turtle].pos")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[0].printify())")
            tkn.props.lines.append("    turtles[current_turtle].pos = pos")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>Ñ)'),
    0, tokenize))

#########################################################################################
# Prints to the screen and resets the cursor.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) and len(tkn.params[0].value):
            tkn.props.lines.append("pos = turtles[current_turtle].pos")
            tkn.props.lines.append("turtles[current_turtle].write(\"" + characters.escape(tkn.params[0].value) + "\")")
            tkn.props.lines.append("turtles[current_turtle].pos = pos")
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    pos = turtles[current_turtle].pos")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[len(stack)-1].printify())")
            tkn.props.lines.append("    turtles[current_turtle].pos = pos")
            tkn.props.lines.append("elif len(B):")
            tkn.props.lines.append("    stack.append(B[len(B)-1])")
            tkn.props.lines.append("    pos = turtles[current_turtle].pos")
            tkn.props.lines.append("    turtles[current_turtle].write(stack[0].printify())")
            tkn.props.lines.append("    turtles[current_turtle].pos = pos")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>ñ)'),
    0, tokenize))

#########################################################################################
# Clears the current turtle.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("turtles[current_turtle].clear()")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>¢)'),
    0, tokenize))

#########################################################################################
# Prints the the current turltes ingoring stacks.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("cout(printify(turtles))")
        
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>£)'),
    0, tokenize))

#########################################################################################
# Equation for Turtle.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params):
            box_match = re.match(r"^(bx)(\d+),?(\d*)$", tkn.params[0].value)
            fill_match = re.match(r"^(fl)(\d+),?(\d*)$", tkn.params[0].value)
            if tkn.params[0].value == "\\":
                tkn.props.lines.append("turtles[current_turtle].move = lambda x,y: (x+1, y+1)")
            elif tkn.params[0].value == "/":
                tkn.props.lines.append("turtles[current_turtle].move = lambda x,y: (x-1, y+1)")
            elif tkn.params[0].value == "|":
                tkn.props.lines.append("turtles[current_turtle].move = lambda x,y: (x, y+1)")
            elif tkn.params[0].value == "-":
                tkn.props.lines.append("turtles[current_turtle].move = lambda x,y: (x, y-1)")
            elif box_match != None:
                width = 0
                height = 0
                if len(box_match.groups()) == 3:
                    cap = box_match.group(0)
                    if cap[len(cap)-1] == "," or len(box_match.group(2)) != 2:
                        width = int(box_match.group(2))
                        height = width
                    else:
                        width = int(box_match.group(2)[0])
                        height = int(box_match.group(2)[1])
                if len(box_match.groups()) == 4:
                    width = int(box_match.group(2))
                    height = int(box_match.group(3))
                name = "box_" + str(tkn.snippet.script.props.identifier)
                tkn.snippet.script.props.identifier += 1
                tkn.props.lines.append(name + " = Extendable()")
                tkn.props.lines.append(name + ".x = turtles[current_turtle].pos[0]")
                tkn.props.lines.append(name + ".y = turtles[current_turtle].pos[1]")
                tkn.props.lines.append(name + ".width = " + str(width))
                tkn.props.lines.append(name + ".height = " + str(height))
                tkn.props.lines.append("turtles[current_turtle].move = lambda x,y: move_box(x,y,"+name+")")
            elif fill_match != None:
                width = 0
                height = 0
                if len(fill_match.groups()) == 3:
                    cap = fill_match.group(0)
                    if cap[len(cap)-1] == "," or len(fill_match.group(2)) != 2:
                        width = int(fill_match.group(2))
                        height = width
                    else:
                        width = int(fill_match.group(2)[0])
                        height = int(fill_match.group(2)[1])
                if len(fill_match.groups()) == 4:
                    width = int(fill_match.group(2))
                    height = int(fill_match.group(3))
                name = "fill_" + str(tkn.snippet.script.props.identifier)
                tkn.snippet.script.props.identifier += 1
                tkn.props.lines.append(name + " = Extendable()")
                tkn.props.lines.append(name + ".x = turtles[current_turtle].pos[0]")
                tkn.props.lines.append(name + ".y = turtles[current_turtle].pos[1]")
                tkn.props.lines.append(name + ".width = " + str(width))
                tkn.props.lines.append(name + ".height = " + str(height))
                tkn.props.lines.append("turtles[current_turtle].move = lambda x,y: move_fill(x,y,"+name+")")
            else:
                tkn.props.lines.append("turtles[current_turtle].move = " + turtle.to_lambda_move_string(tkn.params[0].value))
        else:
            tkn.props.lines.append("if len(stack) > 0:")
            tkn.props.lines.append("    turtles[current_turtle].move = to_lambda_move(stack.pop().value)")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(['+re.escape(characters.printables)+']*)(?P<literal>¤)'),
    0, tokenize))

#########################################################################################
# The most basic loop which is an endless loop.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("while True:")
        tkn.props.lines.append((1, ""))
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ḷ)'),
    0, tokenize))

#########################################################################################
# End of any loop or if statement.
def tokenize(tkn):
    def translator(tkn):
        if tkn.snippet.script.props.indent > 1:
            tkn.props.lines.append((-1, ""))
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>€)'),
    0, tokenize))

#########################################################################################
# Move the turtle a single step.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("turtles[current_turtle].step()")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ʂ)'),
    0, tokenize))

#########################################################################################
# Move the turtle back into the history.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params[0].value):
            tkn.props.lines.append("turtles[current_turtle].step_back_to("+str(base96.whole_base96_to_base10(tkn.params[0].value))+")")
        else:
            tkn.props.lines.append("turtles[current_turtle].step_back()")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ɼ)(['+re.escape(base96.digits)+']?)'),
    0, tokenize))

#########################################################################################
# A command NOOP.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("# NOOP")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>¦)'),
    0, tokenize))

#########################################################################################
# Place top of the stack to the bottom.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("if len(stack):")
        tkn.props.lines.append("    stack.insert(0, stack.pop())")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ȧ)'),
    0, tokenize))

#########################################################################################
# Pop the top of the stack off and throw away.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("if len(stack):")
        tkn.props.lines.append("    stack.pop()")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ḃ)'),
    0, tokenize))

#########################################################################################
# Adds the top two items on the stack.
def tokenize(tkn):
    def translator(tkn):
        if tkn.params[0].value == "":
            tkn.props.lines.append("if len(stack) > 1:")
            tkn.props.lines.append("    popped = stack.pop()")
            tkn.props.lines.append("    popped.add_to(stack.pop())")
            tkn.props.lines.append("    stack.append(popped)")
        elif tkn.params[0].value == "*":
            tkn.props.lines.append("if len(stack) > 1:")
            tkn.props.lines.append("    popped = stack.pop()")
            tkn.props.lines.append("    while len(stack):")
            tkn.props.lines.append("        popped.add_to(stack.pop())")
            tkn.props.lines.append("    stack.append(popped)")
        elif tkn.params[0].value == "s":
            tkn.props.lines.append("if len(stack) > 1:")
            tkn.props.lines.append("    popped = stack.pop()")
            tkn.props.lines.append("    popped.add_to_swap(stack.pop())")
            tkn.props.lines.append("    stack.append(popped)")
        elif tkn.params[0].value == "S":
            tkn.props.lines.append("if len(stack) > 1:")
            tkn.props.lines.append("    popped = stack.pop()")
            tkn.props.lines.append("    while len(stack):")
            tkn.props.lines.append("        popped.add_to_swap(stack.pop())")
            tkn.props.lines.append("    stack.append(popped)")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>⁺)([*sS]?)'),
    0, tokenize))

#########################################################################################
# Flattens a string by characters and floors a number.
def tokenize(tkn):
    def translator(tkn):
        if len(tkn.params) and len(tkn.params[0].value):
            chars = tkn.params[0].value.split('¶')
            if len(chars) == 1:
                chars = list(tkn.params[0].value)
            for c in reversed(chars):
                tkn.props.lines.append("stack.append(ITEM('" + characters.escape(c) + "'))")
        else:
            tkn.props.lines.append("if len(stack):")
            tkn.props.lines.append("    popped = stack.pop()")
            tkn.props.lines.append("    if popped.is_number:")
            tkn.props.lines.append("        popped.value = popped.value.split('¶')[0]")
            tkn.props.lines.append("        stack.append(popped)")
            tkn.props.lines.append("    elif popped.is_string:")
            tkn.props.lines.append("        chars = popped.value.split('¶')")
            tkn.props.lines.append("        if len(chars) == 1:")
            tkn.props.lines.append("            chars = list(popped.value)")
            tkn.props.lines.append("        for c in reversed(chars):")
            tkn.props.lines.append("            stack.append(ITEM(c))")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'([' + re.escape(characters.printables) + u']*)' + u'(?P<literal>ḟ)'),
    0, tokenize))