#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 10:45:13 2017

@author: fanchang
"""
count = 1
fp = open(r'/Users/fanchang/Downloads/Model.txt', 'r')
for line in fp:
	temp = str(line)
	if temp[0:7] == 'C01 P11':
		#        print temp[0:7]
		temp = temp.split(' ')
		#        print str(count), temp[18]
		print temp[18]

		count += 1
fp.close()

# fp = open(r'/Users/fanchang/Downloads/Model.txt','r')
#
# for line in fp:
#    temp = str(line).split(' ')
#    print str(count), temp[17]
#    count +=1
#
# fp.close()
