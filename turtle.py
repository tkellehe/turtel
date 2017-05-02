# -*- coding: UTF-8 -*-
import os
from time import sleep
import re
import math
import characters

EMPTY_STRING = ""

def printify(turtles):
    max_width = 0
    max_height = 0
    for t in turtles:
        if len(t.grid) > max_height:
            max_height = len(t.grid)
        if len(t.grid[0]) > max_width:
            max_width = len(t.grid[0])
    for t in turtles:
        t.expand(max_width, max_height)

    temp = Turtle()
    temp.expand(max_width, max_height)
    for t in turtles:
        for r in range(0, len(t.grid)):
            for c in range(0, len(t.grid[r])):
                if t.grid[r][c] != EMPTY_STRING:
                    temp.grid[r][c] = t.grid[r][c]
    return temp.printify()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
def cout(string):
    cls()
    print(string)
def wait(milliseconds):
    sleep(milliseconds / 1000)

def to_lambda_var_string(var, string):
    if string == "":
        return var
    string = string.replace("~", " " + var + " - ")
    string = string.replace("!", " - " + var + " ")
    string = string.replace("@", " + " + var + " ")
    string = string.replace("&", " ** " + var + " ")
    string = string.replace("^", var + " ** ")
    string = string.replace("d", " / " + var + " ")
    string = string.replace("D", " " + var + " / ")
    string = string.replace("#", "(" + var + "+1)")
    string = string.replace("$", "(" + var + "-1)")
    string = string.replace("p", " math.pi ")
    string = string.replace("t", " (2*math.pi) ")
    string = string.replace("cs", " math.cos( ")
    string = string.replace("sn", " math.sin( ")
    string = string.replace("tn", " math.tan( ")
    string = string.replace("sq", " math.sqrt( ")
    string = string.replace("?", " if ")
    string = string.replace(":", " else ")
    return "(" + string + ")"

def to_lambda(string):
    parts = string.split("`")
    if len(parts) == 1:
        return eval("lambda x: (" + to_lambda_var_string("x", string) + ")")
    if len(parts) == 2:
        return eval("lambda x,y: (" + to_lambda_var_string("x", string) + "," + to_lambda_var_string("y", string) + ")")
    if len(parts) == 3:
        return eval("lambda x,y,z: (" + to_lambda_var_string("x", string) + "," + to_lambda_var_string("y", string) + "," + to_lambda_var_string("z", string) + ")")

def to_lambda_move_string(string):
    parts = string.split("`")
    if len(parts) == 1:
        parsed = to_lambda_var_string("x", parts[0]) + ",y"
    elif len(parts) == 2:
        parsed = to_lambda_var_string("x", parts[0]) + ", " + to_lambda_var_string("y", parts[1])
    else:
        raise Exception("A single '`' is needed for move expressions.")
    return "lambda x,y: (" + parsed + ")"

def to_lambda_move(string):
    return eval(to_lambda_move_string(string))

def on_box_bound(x,y,box):
    if box.x <= x and x < (box.x + box.width) and box.y <= y and y < (box.y + box.height):
        return (x == box.x) or (x == (box.x + box.width - 1)) or (y == box.y) or (y == (box.y + box.height - 1))
    return False


def move_box(x,y,box):
    if not on_box_bound(x,y,box):
        box.x = x
        box.y = y
    if x < (box.x + box.width - 1) and y == box.y:
        return (x+1, y)
    if x == (box.x + box.width - 1) and y < (box.y + box.height - 1):
        return (x, y+1)
    if x > box.x and y == (box.y + box.height - 1):
        return (x-1, y)
    if x == box.x and y > box.y:
        return (x, y-1)


    
class Turtle:
    def __init__(self):
        self.grid = [[" "]]
        self.pos = (0,0)
        self.move = lambda x,y: (x + 1, y)
        self.history_size = len(characters.printables)
        self.history = []
        for i in range(0, self.history_size):
            self.history.append((0,0))
    def printify(self):
        output = ""
        for row in self.grid:
            for c in row:
                output += " " if c == EMPTY_STRING else c
            output += "\n"
        return output[:-1]
    def write(self, value):
        value = str(value)
        for i in value:
            self.single_write(i)
    def clear(self):
        for r in self.grid:
            for i in range(0, len(r)):
                r[i] = EMPTY_STRING
    def step(self):
        old = self.pos
        self.pos = self.move(self.pos[0], self.pos[1])
        self.pos = (int(self.pos[0]), int(self.pos[1]))
        self.history.pop()
        self.history.insert(0, old)
        return old
    def step_back(self):
        old = self.pos
        self.pos = self.history.pop(0)
        self.history.insert(0, old)
        return old
    def step_back_to(self,index):
        old = self.pos
        self.pos = self.history[index%len(self.history)]
        return old
    #####################################################################################
    # Helpers for writing to the grid.
    def insert_row(self, index):
        self.grid.insert(index, [EMPTY_STRING])
        max_len = 0
        for row in self.grid:
            if len(row) > max_len:
                max_len = len(row)
        for row in self.grid:
            while len(row) < max_len:
                row.append(EMPTY_STRING)
    def insert_col(self, row_index, index):
        while len(self.grid) <= row_index:
            self.insert_row(len(self.grid))
        while len(self.grid[row_index]) < index:
            self.grid[row_index].append(EMPTY_STRING)
        self.grid[row_index].insert(index, EMPTY_STRING)
        for row in self.grid:
            row.insert(index, EMPTY_STRING)
        max_len = 0
        for row in self.grid:
            if len(row) > max_len:
                max_len = len(row)
        for row in self.grid:
            while len(row) < max_len:
                row.append(EMPTY_STRING)
    def expand(self, width, height):
        while len(self.grid) < height:
            self.insert_row(len(self.grid))
        max_len = 0
        for row in self.grid:
            if len(row) > max_len:
                max_len = len(row)
        if max_len < width:
            for row in self.grid:
                while len(row) < width:
                    row.append(EMPTY_STRING)
    def single_write(self, char):
        # Also need to see if pos is negative and insert until it is positive.
        if self.pos[1] < 0:
            for i in range(-self.pos[1], 0, -1):
                self.insert_row(0)
            self.pos = (self.pos[0], 0)
        if self.pos[0] < 0:
            for i in range(-self.pos[0], 0, -1):
                self.insert_col(self.pos[1], 0)
            self.pos = (0, self.pos[1])
        if char == "\n":
            self.expand(0, self.pos[1]+1)
            self.pos = (0, self.pos[1]+1)
            self.insert_row(self.pos[1])
        else:
            self.expand(self.pos[0]+1, self.pos[1]+1)
            self.grid[self.pos[1]][self.pos[0]] = char
            self.step()
