#!//anaconda/bin/python
import sys
import os
import numpy as np

filename = r'/Users/fanchang/Desktop/rotation_data'
count =0
with open(filename, 'r') as fp:
	data = fp.read()
	rotation = data.split(',')
	# print len(rotation)
fp.closed

test_record=np.zeros([1, len(rotation)])
print np.shape(test_record)
print test_record
for index in arange(0,len(rotation)):
	print index
	print float(rotation[index].rstrip('\r\n').split('[')[1].rstrip(']'))
	test_record[0,index]=float(rotation[index].rstrip('\r\n').split('[')[1].rstrip(']'))
	# test_record[index,0]=(float(rotation[index].rstrip('\r\n').split('[')[1].rstrip(']')))
print test_record