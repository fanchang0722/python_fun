# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 09:19:13 2016

@author: fanchang
"""

import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 3:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   # print '-'*25+'done'+'-'*25
except:
   print "Error: unable to start thread"

count=0
while 1:
#   count+=1
#   print count
   pass
