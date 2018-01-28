#!/usr/bin/env python
# -*- coding: utf-8 -*-

import regex
import os, sys

'''
Filename: parser_sexpressionV4.py
Description: parse s-expressions converting the structures to arrays
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


def main(fileinput, fileoutput):
    
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
    r = regex.match(patternNum, content)
    if r:
        ref = int(r.group())
        
        s = recursive_bracket_parser(content)
        
        while s:
            
            ltree = eval(content[s[0]:s[1]])
            
            res = 'yes' if is_sum(ltree,ref) else 'no'
            with open(fileoutput, 'a') as f:
                #print res
                f.write(res + '\n')
            
            content = content[s[1]:]
            
            s = []
            r = regex.match(patternNum, content)
            
            if r:
                ref = int(r.group())
                s = recursive_bracket_parser(content)
                s = recursive_bracket_parser(content)
    


if __name__ == '__main__':
    
    fileinput = './input_short'
    fileoutput = './output'
    
    main(fileinput, fileoutput)
    
    