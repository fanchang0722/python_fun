#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:17:39 2017

@author: fanchang
"""
import os
import sys

folder = os.listdir(sys.argv[1])
#print folder
for fileIn in folder:
	if fileIn.endswith('fin'):
#		print fileIn
		fid = open(os.path.join(sys.argv[1], fileIn), 'r')
		lines = fid.readlines()[10:]
		fid.close()
		fout = open(os.path.join(r'C:\Temp\output',fileIn), 'w')
		fout.writelines(lines)
		fout.close()     
		print "file --> " + os.path.join(r'C:\Temp\output',fileIn)		

print "done with reformatting file"

