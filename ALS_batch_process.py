# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 22:32:02 2018

@author: fanchang
"""

import os

folder = r'C:\Users\fanchang\Desktop\A70\ALS\P1dot1\20180306_bringup\20180316_multiple_times_test'

# folder = r'C:\Users\fanchang\Desktop\A70\ALS\P1dot1\GRR\OP2'
fileNames = os.listdir(folder)
for fileName in fileNames:
	if fileName.endswith('csv'):
		#        print os.path.join(folder, fileName)
		fp = open(os.path.join(folder, fileName), 'r')
		fp.readline()
		for line in fp:
			temp = line.rstrip('\r').split(',')
			print temp[0], temp[3]
		# print temp
		# print 2, temp[0],  str(round(float(temp[1]), 5)).rjust(7), str(round(float(temp[2]), 5)).rjust(8), str(round(float(temp[3]), 5)).rjust(7), str(round(float(temp[4]), 5)).rjust(7)
		# print temp[0],  str(round(float(temp[3]), 5)).rjust(7)
