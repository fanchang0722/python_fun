#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:17:39 2017

@author: fanchang
"""
import os
import sys



fid = open(sys.argv[1], 'r')
lines = fid.readlines()[10:]
fid.close()
fout = open(os.path.join(r'C:\Temp\output',sys.argv[1]), 'w')
fout.writelines(lines)
fout.close()      

print "done with reformatting file"
print "file --> " + os.path.join(r'C:\Temp\output',sys.argv[1])
