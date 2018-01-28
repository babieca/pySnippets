#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import parser_sexpressionV1 as psexpV1
import parser_sexpressionV2 as psexpV2
import parser_sexpressionV3 as psexpV3
import parser_sexpressionV4 as psexpV4
import parser_sexpressionV5 as psexpV5
import time, sys
import cProfile

'''
Filename: benchmark.py
Description: measure time of different parser s-expressions algorithms
Version: 0.1
Author: JI
Date: 28/01/2018
Licence: Apache License version 2.0
'''
 
class MyTimer():
 
    def __init__(self, fname):
        self.start = time.time()
        self.fname = fname
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = 'The function took {time} seconds to complete file {fname}'
        print(msg.format(time=runtime, fname=self.fname))

def timeit(fun, fileinput, fileoutput):
    cprof = "cprof_" + fun
    cprof = fileoutput.replace(".main()", ".cprof")
    n = 100
    print("-"*n)
    print('Call: {}'.format(fun))
    cProfile.run(fun + '("' + fileinput + '", "' + fileoutput + '")', cprof)
 
if __name__ == '__main__':
    
    fileinput1 = "./input_short"
    fileinput2 = "./input_large"
    fileoutput = "./output"
    
    timeit("psexpV1.main", fileinput1, fileoutput)
    with MyTimer(fileinput1):
        psexpV1.main(fileinput1, fileoutput)
    with MyTimer(fileinput2):
        psexpV1.main(fileinput2, fileoutput)
    
    timeit("psexpV2.main", fileinput1, fileoutput)
    with MyTimer(fileinput1):
        psexpV2.main(fileinput1, fileoutput)
    with MyTimer(fileinput2):
        psexpV2.main(fileinput2, fileoutput)
    
    timeit("psexpV3.main", fileinput1, fileoutput)
    with MyTimer(fileinput1):
        psexpV3.main(fileinput1, fileoutput)
    with MyTimer(fileinput2):
        psexpV3.main(fileinput2, fileoutput)
        
    timeit("psexpV4.main", fileinput1, fileoutput)
    with MyTimer(fileinput1):
        psexpV4.main(fileinput1, fileoutput)
    with MyTimer(fileinput2):
        psexpV4.main(fileinput2, fileoutput)
    
    timeit("psexpV5.main", fileinput1, fileoutput)
    with MyTimer(fileinput1):
        psexpV5.main(fileinput1, fileoutput)
    with MyTimer(fileinput2):
        psexpV5.main(fileinput2, fileoutput)
    
    sys.exit(0)
    