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
    args.extend(sys.argv[1:])
    for arg in range(0, len(args)):
        args[arg] = itemize(args[arg])
    turtles = [Turtle()]
    stacks = [args,[],[],[],[],[],[],[],[],[]]
    current_stack = 0
    implicit_pop_to_display = True
    current_turtle = 0
    cout(printify(turtles))

"""
footer = """
    if implicit_pop_to_display and len(stacks[current_stack]):
        popped = stacks[current_stack].pop()
        turtles[current_turtle].write(popped.printify())
    cout(printify(turtles))
"""

INDENT = "    "

script = interpreter.Script()

def translate(code):
    script.props.indent = 1
    script.props.identifier = 1
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
        if tkn.literal.value.count(u'¶') == 1:
            tkn.props.lines.append("stacks[current_stack].append(ITEM(\"" + characters.escape(tkn.literal.value) + "\"))")
            tkn.props.lines.append("stacks[current_stack][len(stacks[current_stack])-1].to_number()");
        else:
            tkn.props.lines.append("stacks[current_stack].append(ITEM(\"" + characters.escape(tkn.literal.value) + "\"))")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX("(?P<literal>[" + re.escape(characters.printables) + "]+)"),
    0, tokenize))


#########################################################################################
# Change the current stack.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("current_stack = " + characters.tiny_to_digit(tkn.literal.value))

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX("(?P<literal>[" + re.escape(characters.variables) + "])"),
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
            tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
            tkn.props.lines.append("    wait(stacks[current_stack].pop().to_number().get_value())")

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
                    tkn.snippet.script.tokens[i].props.lasts.append("if len(stacks[current_stack]) > 0:")
                    tkn.snippet.script.tokens[i].props.lasts.append("    wait(stacks[current_stack].pop().to_number().get_value())")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>Ẉ)([shqet]?)'),
    0, tokenize))

#########################################################################################
# Most basic print that consumes from the current stack.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
        tkn.props.lines.append("    turtles[current_turtle].write(stacks[current_stack].pop().printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>Þ)'),
    0, tokenize))

#########################################################################################
# Most basic print that does not consume from the current stack.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
        tkn.props.lines.append("    turtles[current_turtle].write(stacks[current_stack][len(stacks[current_stack])-1].printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>þ)'),
    0, tokenize))

#########################################################################################
# Clears the current turtle then consumes from the current stack to the screen.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("turtles[current_turtle].clear()")
        tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
        tkn.props.lines.append("    turtles[current_turtle].write(stacks[current_stack].pop().printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>Ç)'),
    0, tokenize))

#########################################################################################
# Clears the current turtle then does not consume from the current stack to the screen.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("turtles[current_turtle].clear()")
        tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
        tkn.props.lines.append("    turtles[current_turtle].write(stacks[current_stack][len(stacks[current_stack])-1].printify())")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ç)'),
    0, tokenize))

#########################################################################################
# Prints to the screen and resets the cursor.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
        tkn.props.lines.append("    pos = turtles[current_turtle].pos")
        tkn.props.lines.append("    turtles[current_turtle].write(stacks[current_stack].pop().printify())")
        tkn.props.lines.append("    turtles[current_turtle].pos = pos")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>Ñ)'),
    0, tokenize))

#########################################################################################
# Prints to the screen and resets the cursor.
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
        tkn.props.lines.append("    pos = turtles[current_turtle].pos")
        tkn.props.lines.append("    turtles[current_turtle].write(stacks[current_stack][len(stacks[current_stack])-1].printify())")
        tkn.props.lines.append("    turtles[current_turtle].pos = pos")
        tkn.props.lines.append("cout(printify(turtles))")
    tokenize_basics(tkn)
    tkn.props.is_print_tkn = True
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>ñ)'),
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
            else:
                tkn.props.lines.append("turtles[current_turtle].move = " + turtle.to_lambda_move_string(tkn.params[0].value))
        else:
            tkn.props.lines.append("if len(stacks[current_stack]) > 0:")
            tkn.props.lines.append("    turtles[current_turtle].move = to_lambda_move(stacks[current_stack].pop().value)")

    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(['+re.escape(characters.printables)+']*)(?P<literal>¦)'),
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
# A command NOOP
def tokenize(tkn):
    def translator(tkn):
        tkn.props.lines.append("# NOOP")
        
    tokenize_basics(tkn)
    tkn.translate = translator
script.add(interpreter.Snippet(interpreter.REGEX(u'(?P<literal>¤)'),
    0, tokenize))