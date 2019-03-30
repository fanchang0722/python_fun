# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 17:43:59 2017

@author: fanchang
"""

import datetime
today = datetime.datetime.now()
print("Today's date is {:%Y%m%d_%H%M%S}".format(today))
flag = True
while flag:
    key = input('Key? => ')
    print key
    if key == 4:
        flag = False
        print "done"
#    if key == '1':
#        print ('sfr')
#        flag = True;
#    if key == '2':
#        print ('white')
#        flag = True;
#    if key == '3':
#        print ('dark')
#        flag = True;
#    if key == 'q':
#        print ('quit')
#        flag = False
#    except:
#        print('No such key "%s"!' % key)
#    else:
#        for field in fieldnames:
#            sprint(field.ljust(maxfield), '=>', getattr(record, field))