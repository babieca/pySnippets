#!/usr/bin/env python
# -*- coding: utf-8 -*-

import regex
import os, sys
from string import whitespace

'''
Filename: parser_sexpressionV3.py
Description: parse s-expressions using regular expressions
Version: 0.3
Author: JI
Date: 28/01/2018
Licence: Apache License version 2.0
Input:  the input consists of a sequence of test cases in the form of integer/tree pairs.
        Each test case consists of an integer followed by one or more spaces followed by
        a binary tree formatted as an S-expression as described above.
        All binary tree S-expressions will be valid, but expressions may be spread over
        several lines and may contain spaces. There will be one or more test cases in an
        input file, and input is terminated by end-of-file.
Output: there should be one line of output for each test case (integer/tree pair) in the
        input file. For each pair I,T (I represents the integer, T represents the tree)
        the output is the string yes if there is a root-to-leaf path in T whose sum is I
        and no if there is no path in T whose sum is I.
format: (integer()())...
'''


atom_end = set('()"\'') | set(whitespace)

def parse(sexp):
    stack, i, length = [[]], 0, len(sexp)
    while i < length:
        c = sexp[i]

        reading = type(stack[-1])
        if reading == list:
            if   c == '(': stack.append([])
            elif c == ')': 
                stack[-2].append(stack.pop())
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
            elif c == '"': stack.append('')
            elif c == "'": stack.append([('quote',)])
            elif c in whitespace: pass
            else: stack.append((c,))
        elif reading == str:
            if   c == '"': 
                stack[-2].append(stack.pop())
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
            elif c == '\\': 
                i += 1
                stack[-1] += sexp[i]
            else: stack[-1] += c
        elif reading == tuple:
            if c in atom_end:
                atom = stack.pop()
                if atom[0][0].isdigit(): stack[-1].append(eval(atom[0]))
                else: stack[-1].append(atom)
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
                continue
            else: stack[-1] = ((stack[-1][0] + c),)
        i += 1
    return stack.pop()

def unwrap_list(lst, output = [], node=0):
    if type(lst) == type([]):
        if len(lst) == 3:
            if lst[1]:
                unwrap_list(lst[1], output, node + lst[0])
            if lst[2]:
                unwrap_list(lst[2], output, node + lst[0])
            if not lst[1] and not lst[2]:
                output.append(node + lst[0])


def main(fileinput, fileoutput):
    
    if not os.path.isfile(fileinput):
        print("Error. I could not find the read file %s" %(fileinput))
        sys.exit(1)
    
    with open(fileinput, 'r') as f:
        content = ''.join(line.strip() for line in f)  
    
    content = content.replace(" ", "")
    
    with open(fileoutput, 'w') as f:
        f.write('')

    patternNum = r'(\d+)'
    patternSexp = '\(((?>[^()]+)|(?R))*\)'
    
    r = regex.match(patternNum, content)
    if r:
        ref = int(r.group())
        r = regex.search(patternSexp, content, flags=0)
        while r:
            result = []
            l = r.span()

            parsed = parse(content[l[0]:l[1]])

            unwrap_list(parsed[0], result)

            res = 'yes' if ref in result else 'no'
            with open(fileoutput, 'a') as f:
                #print res
                f.write(res + '\n')
            content = content[l[1]:]
            r = regex.match(patternNum, content)
            if r:
                ref = int(r.group())
                r = regex.search(patternSexp, content, flags=0)
    
if __name__ == '__main__':
    
    fileinput = './input_short'
    fileoutput = './output'
    
    main(fileinput, fileoutput)
    
    