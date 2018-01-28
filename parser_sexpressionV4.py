#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import regex
import os, sys

def recursive_bracket_parser(s, i=0, j=0):
    res = []
    counter = 0
    
    if i < 0: i = 0
    if j == 0  or len(s) < j: j = len(s)
    if i > j: i = j
    
    while i < j:
        if s[i] == '[':
            counter +=1
            if counter == 1: res.append(i)
        elif s[i] == ']':
            counter -=1
            if counter == 0:
                res.append(i+1)
                return res
        i += 1
        
    return []


def is_sum(tree, num):
    if (len(tree) == 0):   # 'in' a leaf
        return False
    if (len(tree[1]) == 0 & len(tree[2]) == 0):   # leaf
        return num == tree[0]
    return (is_sum(tree[1], num-tree[0]) | is_sum(tree[2], num-tree[0]))


if __name__ == '__main__':
    
    fileinput = './input'
    fileoutput = './output'
    
    if not os.path.isfile(fileinput):
        print("Error. I could not find the read file %s" %(fileinput))
        sys.exit(1)
    
    with open(fileinput, 'r') as f:
        content = ''.join(line.strip() for line in f)  
    
    content = content.replace(" ", "")
    content = content.replace('(',',[')
    content = content.replace(')',']')
    
    with open(fileoutput, 'w') as f:
        f.write('')

    patternNum = r'(\d+)'
    patternSexp = '\[([^()]|(?R))*\]'
    
    r = regex.match(patternNum, content)
    if r:
        ref = int(r.group())
        
        s = recursive_bracket_parser(content)
        
        while s:
            
            ltree = eval(content[s[0]:s[1]])
            
            res = 'yes' if is_sum(ltree,ref) else 'no'
            with open(fileoutput, 'a') as f:
                print res
                f.write(res + '\n')
            
            content = content[s[1]:]
            
            s = []
            r = regex.match(patternNum, content)
            
            if r:
                ref = int(r.group())
                s = recursive_bracket_parser(content)
                s = recursive_bracket_parser(content)
    
