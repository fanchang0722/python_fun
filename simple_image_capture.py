#!/usr/bin/python
"""A simple image capture."""
import time
import logging
import openhtf
from openhtf.plugs import usb
from openhtf.names import *
import subprocess

@plug(adb=usb.AdbPlug)
def TestADBPhase(test, adb):
    """
    Simple test to communicate with ADB
    """
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
    logging.debug('testADBPhase start!!!!')
    
#    test.logger.info('shell response %s', out)
#    print 2
#    proc = subprocess.Popen(["adb kill-server"], stdout=subprocess.PIPE, shell=True)
#    (out, err) = proc.communicate()
#    test.logger.info('shell response is %s', out)
#    print 3
    response = adb.Shell('ls /data/user')
    print response
    test.logger.info('file path %s', response)

PHASES = [TestADBPhase,]


def TestStart():
    dutId = prompts.DisplayPrompt('type dutID')
    return dutId

if __name__ == '__main__':
    logging.basicConfig(filename='fan_example.log',filemode='w',level=logging.DEBUG)
    test = openhtf.Test(*PHASES)
    test.AddOutputCallback(OutputToJSON('./%(dut_id)s.%(start_time_millis)s', indent=4))
    test.Execute(test_start=TestStart)
