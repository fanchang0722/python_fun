# -*- coding: utf-8 -*-
"""
Created on Mon May 22 11:50:04 2017

@author: fanchang
"""

import json
import os

import numpy as np

folder = r'//Users/fanchang/Google Drive/A50/A50_EVT/Asub/light/20170405/image/Results'
files = os.listdir(folder)
Blemkey = 'blemishResults'
subkeys = ['Optical_ctr_offset_radial_PXLS_PCT']


# distkey = 'distance_Pct'
# Ny4key = 'secondary_1_results'
# Ny2key = 'secondary_2_results'


def array_concate(input1, input2):
	temp = np.array([])
	temp = np.hstack((temp, input1))
	return np.hstack((temp, input2))


fd = open(os.path.join(os.getcwd(), 'Asub_EVT_OC_' + folder.split('/')[9] + '.csv'), 'w')
fd.write('SN,Date,Time,Center, UL, LL, UR, LR\n')
output = np.array([])
count = 1
for filename in files:
	if filename.endswith('json') and filename.startswith('LOE6500'):
		print(filename)
		temp = np.array([])
		result = json.load(open(os.path.join(folder, filename)))
		name, timestamp = filename.split('_')[0:2]
		for subkey in subkeys:
			temp = np.hstack((temp, np.array(result[Blemkey][subkey])[0]))

		output = array_concate(name, folder.split('/')[9])
		output = array_concate(output, timestamp)
		output = array_concate(output, temp)
		print count
		count += 1
		print(output.T)
		for index in range(len(output)):
			fd.write(str(output[index]) + ',')
		fd.write('\n')
fd.close()
print(os.path.join(os.getcwd(), 'Asub_EVT_OC_' + folder.split('/')[9] + '.csv'))
