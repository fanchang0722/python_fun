#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:17:39 2017

@author: fanchang
"""
import os
import sys

folder = os.listdir(sys.argv[1])
for fileIn in folder:
    if fileIn.endswith('txt'):
        fid = open(os.path.join(sys.argv[1], fileIn), 'r')
        for line in fid:
            temp = line.rstrip('\r\n')
            if temp[0] != '#':
                temp_str=temp.split(' ')

count = 0
for fileIn in folder:
	if fileIn.endswith('fin'):
		fid = open(os.path.join(sys.argv[1], fileIn), 'r')
		lines = fid.readlines()[10:]
		fid.close()
		fout = open(os.path.join(r'/Users/fanchang/Downloads/tmp',sys.argv[2]+'_'+str(int(float(temp_str[count])*1000000))
+'.fih'), 'w')
		fout.writelines(lines)
		fout.close()   
        count += 1	
        if count > len(folder)-1:
            break
print "done with reformatting file"

