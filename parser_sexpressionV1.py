#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import sys
import os

'''
Notes:
    Note that with this formulation all leaves of a tree are of the form (integer () () )

    Since an empty tree has no root-to-leaf paths, any query as to whether a path exists
    whose sum is a specified integer in an empty tree must be answered negatively.

The Input

    The input consists of a sequence of test cases in the form of integer/tree pairs.
    Each test case consists of an integer followed by one or more spaces followed by
    a binary tree formatted as an S-expression as described above.
    All binary tree S-expressions will be valid, but expressions may be spread over
    several lines and may contain spaces. There will be one or more test cases in an
    input file, and input is terminated by end-of-file.

Sample Input

    22 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))
    
    20 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))
    
    10 (3
    
         (2 (4 () () )
    
            (8 () () ) )
    
         (1 (6 () () )
    
            (4 () () ) ) )
    
    5 ()

 

The Output

    There should be one line of output for each test case (integer/tree pair) in the
    input file. For each pair I,T (I represents the integer, T represents the tree)
    the output is the string yes if there is a root-to-leaf path in T whose sum is I
    and no if there is no path in T whose sum is I.
 
Sample Output

    yes
    
    no
    
    yes
    
    no
'''

pattern = '(integer () () )'

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

def flatten(dictionary):
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            # recurse
            for res in flatten(value):
                yield res
        else:
            yield len(dictionary.keys()), value

def GetKeyFromDictByValue(self, dictionary, value_to_find):
    for key, value in flatten(dictionary):
        if (value == value_to_find) and (key == 1):
            return key

def walkdown(tree, nodes, total=0):
    if len(nodes) == 0: return tree
    
    node_name = nodes[0]
    i = int(node_name)
    if tree and node_name in tree:
        tree[node_name] = walkdown(tree[node_name], nodes[1:], tree[node_name]['sum'])
    else:
        tree[node_name] = {'sum': int(total) + i}
    return tree 

node_name = ''
parent_names = []
ref = []
tree = {}
counter = 0
k = 0
while k < len(content):
    ch = content[k]
    if ch == '(':
        if counter == 0:
            ref = int(node_name)
        else:
            parent_names.append(node_name)
            tree = walkdown(tree, parent_names)
        node_name = ''
        counter +=1
    elif ch == ')':
        counter -=1
        if counter == 0:
            node_name = ''
            res = 'yes' if GetKeyFromDictByValue(None, tree, ref) == 1 else 'no'
            with open(fileoutput, 'a') as f:
                print res
                f.write(res + '\n')
            tree = {}
        else:
            node_name = parent_names.pop()
    else:
        node_name = node_name + ch
    
    k +=1

sys.exit(0)
