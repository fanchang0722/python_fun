# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 21:41:11 2016

@author: fanchang
"""

s='aardvark'
print s
temp=[s[0]]
count=0
for index in range(1,len(s)):
#    print s[index]
    if s[index] in list(s)[:index]:
        temp.append('*') 
    else:
        temp.append(s[index])
print "".join(temp)
