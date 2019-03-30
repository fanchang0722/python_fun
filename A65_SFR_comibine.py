#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:01:26 2017

@author: fanchang
"""

import os

folder = r'/Users/fanchang/CommonUtils'
fp = open('A65_P0_6DoF_SFR.csv', 'a')
fp.writeline('Camera SN, Date, HMS,	location, Ny, C_H, TL_H, TR_H, BL_H, BR_H,	C_V, TL_V,	TR_V, BL_V,	BR_V')
for filename in os.listdir(folder):
	if filename.endswith('left_NY4.csv'):
		temp = filename.split('_')
		with open(os.path.join(folder, filename), 'r') as csvfile:
			data = csvfile.readline().rstrip('\n')
		csvfile.close()
		fp.write(temp[1] + ',' + temp[2] + ',' + temp[3] + ',left,' + data + '\n')
fp.close()
