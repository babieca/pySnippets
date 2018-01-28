#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import regex
import os, sys
 
dbg = False
 
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
    if dbg: print("%-6s %-14s %-44s %-s" % tuple("term value out stack".split()))
    for termtypes in regex.finditer(term_regex, sexp):
        term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]
        if dbg: print("%-7s %-14s %-44r %-r" % (term, value, out, stack))
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

            parsed = parse_sexp(content[l[0]:l[1]])
            
            unwrap_list(parsed, result)
            res = 'yes' if ref in result else 'no'
            with open(fileoutput, 'a') as f:
                print res
                f.write(res + '\n')
            content = content[l[1]:]
            r = regex.match(patternNum, content)
            if r:
                ref = int(r.group())
                r = regex.search(patternSexp, content, flags=0)
    
