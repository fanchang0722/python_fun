# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:41:21 2016

@author: fanchang
"""

import subprocess
print '-'*5+"Add adb devices"+'-'*5
proc =subprocess.Popen('adb devices',stdout=subprocess.PIPE,shell=True)
(out,err)=proc.communicate()
print 1
print out
print err
#print "out1" + out
#print "err1" + err

print '-'*5+"List ps"+'-'*5
proc =subprocess.Popen('ps |grep adb',stdout=subprocess.PIPE,shell=True)
(out,err)=proc.communicate()
print 2
print out
print err

print '-'*5+"Push Unix shell script to Adb device"+'-'*5
proc = subprocess.Popen(["adb push /usr/local/google/home/fanchang/Downloads/cameratest.sh /data/user"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print 3
print out
print err

print '-'*5+"Stop Adb devices"+'-'*5
proc = subprocess.Popen(["adb kill-server"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print 4
print out
print err

print '-'*5+"List ps"+'-'*5
proc =subprocess.Popen('ps',stdout=subprocess.PIPE,shell=True)
(out,err)=proc.communicate()
print 5
print out
print err


print '-'*25+'done'+'-'*25