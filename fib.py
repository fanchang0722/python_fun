# -*- coding: utf-8 -*-
"""
Created on Sat Mar 03 23:59:10 2018

@author: fanchang
"""

def fib(n):
    a, b = 1, 1
#    b = 1
    for i in range(n):
        a, b = b, a+b
    return a

for i in range(10):
    print "The fib number of %d is %2d" % (i, fib(i))