# from sympy import symbols
# from sympy.logic import SOPform
# from sympy.logic import gateinputcount
from sympy import *
from sympy.logic import *
from pprint import pprint

char_map = {
    0: 0b01111110,
    1: 0b00110000,
    2: 0b01101101,
    3: 0b01111001,
    4: 0b00110011,
    5: 0b01011011,
    6: 0b01011111,
    7: 0b01110000,
    8: 0b01111111,
    9: 0b01111011,

    ' ': 0b00000000,
    '0': 0b01111110,
    '1': 0b00110000,
    '2': 0b01101101,
    '3': 0b01111001,
    '4': 0b00110011,
    '5': 0b01011011,
    '6': 0b01011111,
    '7': 0b01110000,
    '8': 0b01111111,
    '9': 0b01111011,
    'A': 0b01110111,
    'B': 0b00011111,
    'C': 0b01001110,
    'D': 0b00111101,
    'E': 0b01001111,
    'F': 0b01000111,
    'G': 0b01011110,
    'H': 0b00110111,
    'I': 0b00000110,
    'J': 0b00111100,
    'K': 0b01010111,
    'L': 0b00001110,
    'M': 0b01010100,
    'N': 0b01110110,
    'O': 0b01111110,
    'P': 0b01100111,
    'Q': 0b01101011,
    'R': 0b01100110,
    'S': 0b01011011,
    'T': 0b00001111,
    'U': 0b00111110,
    'V': 0b00111110,
    'W': 0b00101010,
    'X': 0b00110111,
    'Y': 0b00111011,
    'Z': 0b01101101,
    'a': 0b01111101,
    'b': 0b00011111,
    'c': 0b00001101,
    'd': 0b00111101,
    'e': 0b01101111,
    'f': 0b01000111,
    'g': 0b01111011,
    'h': 0b00010111,
    'i': 0b00000100,
    'j': 0b00011000,
    'k': 0b01010111,
    'l': 0b00000110,
    'm': 0b00010100,
    'n': 0b00010101,
    'o': 0b00011101,
    'p': 0b01100111,
    'q': 0b01110011,
    'r': 0b00000101,
    's': 0b01011011,
    't': 0b00001111,
    'u': 0b00011100,
    'v': 0b00011100,
    'w': 0b00010100,
    'x': 0b00110111,
    'y': 0b00111011,
    'z': 0b01101101,
    '{': 0b00110001,
    '|': 0b00000110,
    '}': 0b00000111,
    '~': 0b01000000
}

catchphrase = "WhAt thE FISh"

padded = ("_"+catchphrase).ljust(16, "_")

table = []


def tobits(mask: int):
    out = [0, 0, 0, 0, 0, 0, 0]
    for bit in range(0, 7):
        if mask & (1 << bit):
            out[6-bit] = 1
    return out


for i in range(0, 1 << 4):
    char = "N/A"
    bits = ["X"] * 7
    if 0 < i <= len(catchphrase):
        char = catchphrase[i - 1]
        bits = tobits(char_map[char])
    table.append(bits)


def bitlist(n: int):
    return [int(c) for c in f'{n:04b}']


segment_table = list(zip(*table))

h, k, m, p = symbols("h k m p")
wildcards = [bitlist(0), bitlist(14), bitlist(15)]

aoi_sops = {}
for segment in segment_table:
    minterms = []
    for i, value in enumerate(segment):
        if value == 0:
            minterms.append(i)
    sop = SOPform([h, k, m, p], minterms, wildcards)
    aoi_sops[sop] = gateinputcount(sop)
print(sum(aoi_sops.values()))


def conversion(bin_func, *args):
    if len(args) == 2:
        return bin_func(*args)
    return conversion(bin_func, bin_func(*args[:2]), *args[2:])


def nand_and(left, right):
    with evaluate(False):
        return Nand(Nand(left, right), Nand(left, right))


def nand_or(left, right):
    with evaluate(False):
        return Nand(Nand(left, left), Nand(right, right))


nand_sops = {}
with evaluate(False):
    for sop in aoi_sops.keys():
        nand_sop = sop.replace(Not, lambda arg: Nand(arg, arg)).replace(
            And, lambda *args: conversion(nand_and, *args)).replace(Or, lambda *args: conversion(nand_or, *args))
        nand_sops[nand_sop] = gateinputcount(nand_sop)
        print(f'UNSIMP {nand_sop}')

print(sum(nand_sops.values()))
