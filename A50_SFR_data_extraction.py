# -*- coding: utf-8 -*-
"""
Created on Mon May 22 11:50:04 2017

@author: fanchang
"""

import json
import os

import numpy as np

folder = r'//Users/fanchang/Downloads/A50_DVT/FATP_corre/20170624-focus-f3/image/Results/'
# folder = r'/usr/local/google/home/fanchang/Downloads/A50 DVT 21pcs special \selected camera data/20170613/checkfocus/image/Results/'
files = os.listdir(folder)
SFRkey = 'sfrplusResults'
subkeys = ['distance_Pct', 'secondary_1_results', 'secondary_2_results']


# distkey = 'distance_Pct'
# Ny4key = 'secondary_1_results'
# Ny2key = 'secondary_2_results'


def array_concate(input1, input2):
	temp = np.array([])
	temp = np.hstack((temp, input1))
	return np.hstack((temp, input2))


fd = open(os.path.join(os.getcwd(), 'FATP3_DVT_corr' + folder.split('/')[7] + '.csv'), 'w')
fd.write(
	'SN,Date,Time,CH,TLH,BLH,TRH,BRH,CV,TLV,BLV,TRV,BRV,NY4_CH,NY4_TLH,NY4_BLH,NY4_TRH,NY4_BRH,NY4_CV,NY4_TLV,NY4_BLV,NY4_TRV,NY4_BRV,NY2_CH,NY2_TLH,NY2_BLH,NY2_TRH,NY2_BRH,NY2_CV,NY2_TLV,NY2_BLV,NY2_TRV,NY2_BRV\n')
output = np.array([])
count = 1
for filename in files:
	if filename.endswith('json') and filename.startswith('LOE6500'):
		print(filename)
		temp = np.array([])
		result = json.load(open(os.path.join(folder, filename)))
		name, timestamp = filename.split('_')[0:2]
		for subkey in subkeys:
			temp = np.hstack((temp, np.array(result[SFRkey][subkey])))
		output = array_concate(name, folder.split('/')[7])
		output = array_concate(output, timestamp)
		output = array_concate(output, temp)
		print count
		count += 1
		print(output.T)
		for index in range(len(output)):
			fd.write(str(output[index]) + ',')
		fd.write('\n')
fd.close()
print(os.path.join(os.getcwd(), 'Asub_DVT_' + folder.split('/')[7] + '.csv'))
