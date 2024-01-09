from sympy import symbols
from sympy.logic import SOPform
from prettytable import PrettyTable
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

seg_display: list[str] = [
    " --- ",
    "|   |",
    " --- ",
    "|   |",
    " --- "]


def output(mask: int):
    out = seg_display[:]
    for bit in range(0, 7):
        if not (mask & (1 << bit)):
            match 6 - bit:
                case 0:
                    out[0] = "     "
                case 1:
                    out[1] = out[1][:-1] + " "
                case 2:
                    out[3] = out[3][:-1] + " "
                case 3:
                    out[4] = "     "
                case 4:
                    out[3] = " " + out[3][1:]
                case 5:
                    out[1] = " " + out[1][1:]
                case 6:
                    out[2] = "     "
    print("\n".join(out))


def tobits(mask: int):
    out = [0, 0, 0, 0, 0, 0, 0]
    for bit in range(0, 7):
        if mask & (1 << bit):
            out[6-bit] = 1
    return out


catchphrase = "WhAt thE FISh"
# for char in catchphrase:
#     output(char_map[char])

padded = ("_"+catchphrase).ljust(16, "_")
# Color
R = "\033[0;31;40m"  # RED
G = "\033[0;32;40m"  # GREEN
Y = "\033[0;33;40m"  # Yellow
B = "\033[0;34;40m"  # Blue
RB = "\[\033[41m\]"
GB = "\[\033[42m\]"
YB = "\[\033[43m\]"
BB = "\[\033[44m\]"
N = "\033[0m"  # Reset

table = PrettyTable(["H", "K", "M", "P", "CHAR", "a",
                    "b", "c", "d", "e", "f", "g"])


def get_table_entry(table: PrettyTable, i: int, field: str):
    row = table[i]
    row.border = False
    row.header = False
    return row.get_string(fields=[field]).strip()


def get_main_table_entry(i: int, field: str):
    return get_table_entry(table, i, field)


table2 = []

for i in range(0, 1 << 4):
    char = "N/A"
    bits = ["X"] * 7
    if 0 < i <= len(catchphrase):
        char = catchphrase[i - 1]
        bits = tobits(char_map[char])
    # print(bits)
    table2.append(bits)
    table.add_row([*f"{i:04b}", char, *bits])
# print(table)

segments = {}

for segment in range(0, 7):
    char = chr(97+segment)
    karnaugh = PrettyTable([char, "!M!P", "!MP", "MP", "M!P"])

    def entries(offset: int):
        return [get_main_table_entry(offset + 0, char), get_main_table_entry(offset + 1, char), get_main_table_entry(offset + 3, char), get_main_table_entry(offset + 2, char)]

    karnaugh.add_row(["!H!K", *entries(0)])
    karnaugh.add_row(["!HK", *entries(4)])
    karnaugh.add_row(["HK", *entries(12)])
    karnaugh.add_row(["H!K", *entries(8)])
    segments[char] = karnaugh

# for segment, karnaugh in segments.items():
#     print(karnaugh)


def bitlist(n: int):
    return [int(c) for c in f'{n:04b}']


segment_table = list(zip(*table2))

h, k, m, p = symbols("h k m p")
wildcards = [bitlist(0), bitlist(14), bitlist(15)]

for segment in segment_table:
    print(segment)
    minterms = []
    for i, value in enumerate(segment):
        if value == 0:
            minterms.append(i)
    print(SOPform([h, k, m, p], minterms, wildcards))
