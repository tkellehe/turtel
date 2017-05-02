# -*- coding: UTF-8 -*-
import re

def __get_groupindex__(match):
    result = dict()
    for name in match.groupdict():
        start = match.start(name)
        if start == -1:
            result[name] = None
            continue
        end = match.end(name)
        for index in range(0, len(match.groups())):
            index = index + 1
            if start == match.start(index) and end == match.end(index):
                result[name] = index
                break
    return result


Extendable = type('Extendable', (object,), {})

def REGEX(rstring):
    return re.compile(u"^" + rstring + u"$")

##########################################################################################
class Symbol:
    def __init__(self, token, captured, start, end):
        self.props = Extendable()
        self.token = token
        self.value = captured
        self.start = start
        self.end = end

##########################################################################################
class Token:
    def __init__(self, match, code, start, end):
        self.props = Extendable()
        self.symbols = dict()
        self.params = []
        self.code = code
        self.start = start
        self.end = end
        self.captured = match.group(0)
        self.literal = None
        self.index = None
        self.snippet = None
        groupnames = match.groupdict()
        # Now get the symbols.
        for name in groupnames:
            if name == "literal":
                self.literal = Symbol(self,
                                      match.group("literal"),
                                      match.start("literal"),
                                      match.end("literal"))
            elif match.group(name) != None:
                self.symbols[name] = Symbol(self,
                                      match.group(name),
                                      match.start(name),
                                      match.end(name))
            else:
                self.symbols[name] = None
        # Now get the params.
        for param in range(0, len(match.groups())):
            param += 1
            ignore = False
            for name in groupnames:
                if match.group(name) != None and match.start(param) == match.start(name):
                    ignore = True
                    break
            if ignore:
                continue
            self.params.append(Symbol(self,
                                      match.group(param),
                                      match.start(param),
                                      match.end(param)))
    def translate(self):
        pass

##########################################################################################
# Is the actual parser that will generate the Tokens.
class Snippet:
    def __init__(self, regex, priority = None, traverse = None):
        self.props = Extendable()
        self.regex = regex
        self.priority = 0 if priority == None else priority
        self.script = None
        self.traverse = self.donothing if traverse == None else traverse
    def parse(self, code, start, end):
        match = self.regex.match(code[start:end])
        if(match != None):
            token = Token(match, code, start, end)
            token.snippet = self
            r = self.traverse(token)
            return token if r == None or r == True else None
        return None
    def donothing(self, token):
        pass

##########################################################################################
# Is the actual parser that will generate the Tokens.
class Script:
    def __init__(self):
        self.props = Extendable()
        self.snippets = []
        self.tokens = []
    def add(self, snippet):
        snippet.script = self
        self.snippets.append(snippet)
    def parse(self, code):
        index = 0
        while index < len(code):
            end = index
            tkn = None
            while end < len(code):
                for snippet in self.snippets:
                    temp = snippet.parse(code, index, end+1)
                    if tkn == None:
                        tkn = temp
                    elif temp != None and temp.snippet.priority >= tkn.snippet.priority:
                        tkn = temp
                end += 1

            # Selected the token that makes the most sense out of the most characters.
            # Now can place onto the list of tokens.
            if tkn != None:
                tkn.index = len(self.tokens)
                self.tokens.append(tkn)
                index = tkn.end
            else:
                index += 1

        # All of the tokens now have been packed.
        for tkn in self.tokens:
            tkn.translate(tkn)