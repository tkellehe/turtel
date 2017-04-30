# -*- coding: UTF-8 -*-
import re
def escape(string):
    return string.replace("\\", "\\\\").replace("\n", "\\n").replace("\"", "\\\"").replace("'", "\\'")

def tiny_to_digit(string):
    output = ""
    for c in string:
        output += map_tiny_to_digit[c]
    return output

characters = """
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶ẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏżƁƇƊƑƓƘƝƤƬƲȤɓƈɗƒɠƙɲƥƭʋȥɦɱʠɼʂÆÇÑØŒÞæçñøœþßÐıȷ°¹²³⁴⁵⁶⁷⁸⁹¦©®«»‘’“”¤€¢£¥µ…¬¡¿×÷⁺⁻⁼⁽⁾"""

printables = """
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""

specials = "ƁƇƊƑƓƘƝƤƬƲȤɓƈɗƒɠƙɲƥƭʋȥ"

actions = "ɦɱʠɼʂ"

basics = "ẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż"

operators = "¦©®«»‘’“”¤€¢£¥µ…¬¡¿×÷⁺⁻⁼⁽⁾"

variables = "°¹²³⁴⁵⁶⁷⁸⁹"
map_tiny_to_digit = dict()
for i in range(0, len(variables)):
    map_tiny_to_digit[variables[i]] = str(i)

displays = "ÆÇÑØŒÞæçñøœþ"

mutators = "ßÐıȷ"

decimal = "¶"