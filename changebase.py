#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import string

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def is_binary(s):
    return all((ord(c) == 48 or ord(c) == 49) for c in s)

def is_hex(s):
    return all(c in string.hexdigits for c in s)

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Insert arg 1 (binary/dec/hex) and arg 2 (int) as base to convert")

    iput = sys.argv[1]

    if len(sys.argv) == 2:
        if is_binary(iput):
            print(int(iput, 2))
        else:
            print("Missing arg 2 (int) as base to convert")
        sys.exit(0)

    base = sys.argv[2]

    if int(base) < 2:
        print("Arg2 (base) must be > 1")
        sys.exit(0)

    if iput.isdigit():
        print(baseN(int(iput), int(base)))
    elif is_hex(iput):
        print(baseN(int(iput,16), int(base)))
    else:
        print("Arg1 must be binary, decimal or hex")

    sys.exit(0)
