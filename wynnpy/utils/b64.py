

def b64fromINTN(a: int, length: int) -> str:
    """
    Convert integer `a` to its base64 representation string of given length 
    If specified length is bigger than length of result, add trailing zeroes
    Else returns `length` least signigicant digits
    """
    
    alphabet64 = {0 : r"0",
                    1 : r"1",
                    2 : r"2",
                    3 : r"3",
                    4 : r"4",
                    5 : r"5",
                    6 : r"6",
                    7 : r"7",
                    8 : r"8",
                    9 : r"9",
                    10: r"A",
                    11: r"B",
                    12: r"C",
                    13: r"D",
                    14: r"E",
                    15: r"F",
                    16: r"G",
                    17: r"H",
                    18: r"I",
                    19: r"J",
                    20: r"K",
                    21: r"L",
                    22: r"M",
                    23: r"N",
                    24: r"O",
                    25: r"P",
                    26: r"Q",
                    27: r"R",
                    28: r"S",
                    29: r"T",
                    30: r"U",
                    31: r"V",
                    32: r"W",
                    33: r"X",
                    34: r"Y",
                    35: r"Z",
                    36: r"a",
                    37: r"b",
                    38: r"c",
                    39: r"d",
                    40: r"e",
                    41: r"f",
                    42: r"g",
                    43: r"h",
                    44: r"i",
                    45: r"j",
                    46: r"k",
                    47: r"l",
                    48: r"m",
                    49: r"n",
                    50: r"o",
                    51: r"p",
                    52: r"q",
                    53: r"r",
                    54: r"s",
                    55: r"t",
                    56: r"u",
                    57: r"v",
                    58: r"w",
                    59: r"x",
                    60: r"y",
                    61: r"z",
                    62: r"+",
                    63: r"-"}
    
    #  a[n]*base^n + a[n-1]*base^(n-1) + . . . + a[1]*base^1 + a0*base^0
    result = ""
    while a > 0:
        remainder = a % 64
        digit64 = alphabet64[remainder]
        result = digit64 + result
        a = a // 64
    if len(result) > length:
        result = result[-length::]
    elif len(result) < length:
        result = "0" * (length - len(result)) + result
    return result