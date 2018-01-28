#!/usr/bin/env python
# -*- coding: utf-8 -*-

import regex
import os, sys

'''
Filename: parser_sexpressionV2.py
Description: parse s-expressions using regular expressions
Version: 0.2
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
 
term_regex = r'''(?mx)
    \s*(?:
        (?P<brackl>\()|
        (?P<brackr>\))|
        (?P<num>\-?\d+\.\d+|\-?\d+)|
        (?P<sq>"[^"]*")|
        (?P<s>[^(^)\s]+)
       )'''
 
def parse_sexp(sexp):
    stack = []
    out = []

    for termtypes in regex.finditer(term_regex, sexp):
        term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]

        if   term == 'brackl':
            stack.append(out)
            out = []
        elif term == 'brackr':
            assert stack, "Trouble with nesting of brackets"
            tmpout, out = out, stack.pop(-1)
            out.append(tmpout)
        elif term == 'num':
            v = float(value)
            if v.is_integer(): v = int(v)
            out.append(v)
        elif term == 'sq':
            out.append(value[1:-1])
        elif term == 's':
            out.append(value)
        else:
            raise NotImplementedError("Error: %r" % (term, value))
    assert not stack, "Trouble with nesting of brackets"
    return out[0]
 
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

            parsed = parse_sexp(content[l[0]:l[1]])
            
            unwrap_list(parsed, result)
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
    
