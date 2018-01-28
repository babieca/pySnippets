#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import regex
import os, sys
from string import whitespace

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


if __name__ == '__main__':
    
    fileinput = './input'
    fileoutput = './output'
    
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
                print res
                f.write(res + '\n')
            content = content[l[1]:]
            r = regex.match(patternNum, content)
            if r:
                ref = int(r.group())
                r = regex.search(patternSexp, content, flags=0)
    
