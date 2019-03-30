# -*- coding: utf-8 -*-
"""
Created on Mon May 22 11:50:04 2017

@author: fanchang
"""

import json
import os

import numpy as np

SFRkey = 'sfrplusResults'
subkeys = ['distance_Pct', 'secondary_1_results', 'secondary_2_results']


def array_concate(input1, input2):
	temp = np.array([])
	temp = np.hstack((temp, input1))
	return np.hstack((temp, input2))


mainfolder = r'/usr/local/google/home/fanchang/Documents/A50/EVT/FATP/focus/'
folders = os.listdir(mainfolder)
for folder in folders:
	# folder = r'/usr/local/google/home/fanchang/Documents/A50/EVT/Asub/focus/20170417/image/Results/'
	files = os.listdir(os.path.join(mainfolder, folder + '/image/Results/'))
	print(folder)
	#    print(files)
	#
	#
	fd = open(os.path.join(os.getcwd(), 'FATP_Focus_' + folder + '.csv'), 'w')
	fd.write(
		'SN,Date,Time,CH,TLH,BLH,TRH,BRH,CV,TLV,BLV,TRV,BRV,NY4_CH,NY4_TLH,NY4_BLH,NY4_TRH,NY4_BRH,NY4_CV,NY4_TLV,NY4_BLV,NY4_TRV,NY4_BRV,NY2_CH,NY2_TLH,NY2_BLH,NY2_TRH,NY2_BRH,NY2_CV,NY2_TLV,NY2_BLV,NY2_TRV,NY2_BRV\n')

	for filename in files:
		if filename.endswith('json') and filename.startswith('LOE6500'):
			print(files)
			#            time.sleep(0.2)
			temp = np.array([])
			output = np.array([])
			result = json.load(open(os.path.join(mainfolder, folder + '/image/Results/' + files[0])
			                        ))
			name, timestamp = filename.split('_')[0:2]
			for subkey in subkeys:
				temp = np.hstack((temp, np.array(result[SFRkey][subkey])))
			output = array_concate(name, folder)
			output = array_concate(output, timestamp)
			output = array_concate(output, temp)
			#            print(output.T)
			for index in range(len(output)):
				fd.write(str(output[index]) + ',')
			fd.write('\n')
	fd.close()
#
