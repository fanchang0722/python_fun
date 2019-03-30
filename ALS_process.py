# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:17:05 2018

@author: fanchang
"""
import time

import numpy as np


def ALS_calibration(fileName, polyOrder, criteria):
	fp = open(fileName, 'r')
	fp.readline()
	count = 1
	LED = np.zeros([4, ])
	ALS = np.zeros([4, ])
	index = 0
	for line in fp:
		temp = line.rstrip('\r\n').split(',')
		if count % 5:
			LED[index] += float(temp[4])
			ALS[index] += float(temp[6])
		else:
			index += 1
		count += 1
	fp.close()
	LED = LED / 5.0
	ALS = ALS / 5.0
	linearFit = np.polyfit(ALS[0:3], LED[0:3], polyOrder)
	#    linearFit = np.polyfit(LED[0:3], ALS[0:3], polyOrder)
	slope = linearFit[0]
	intercept = linearFit[1]
	p = np.poly1d(linearFit)
	pfit = p(LED[3])
	result = 100.0 * abs(pfit - ALS[3]) / ALS[3]
	#    print temp[5], result
	if result <= criteria:
		return (temp[5], slope, intercept, 'pass')
	else:
		return (temp[5], slope, intercept, 'fail')


fileName = r'C:\Users\fanchang\Desktop\als_test_records_20180130\test_records_20180130'
(SN, slope, intercept, result) = ALS_calibration(fileName, 1, 100)
print SN
print slope
print intercept
print result
outputFile = SN + '_' + time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '_result.csv'
print outputFile
fout = open(outputFile, 'w')
fout.writelines('SN,Slope,Intercept,Pass/Fail\r')
fout.writelines(SN + ',' + str(slope) + ',' + str(intercept) + ',' + result + '\r')
fout.close()
