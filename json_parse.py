# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 11:02:06 2016

@author: fanchang
"""

import sys
import numpy as np

fp = open(r'/Users/fanchang/Desktop/DUT#_05_uni_result.json','r')
result_dict = dict()
line_number = 0
for line in fp:    
    temp = line.rstrip('\r\n')
    temp2 = temp.split('":')
    if len(temp2) >= 2:
#        print str(line_number)+'-->'+temp2[0].lstrip('\t')[1:]
#        print str(line_number)+'-->'+temp2[1]
        result_dict[temp2[0].lstrip('\t')[1:]] = temp2[1]
        line_number+=1
fp.close()
