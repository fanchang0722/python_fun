#!/usr/bin/python
"""A simple test."""

import logging
import openhtf
from openhtf.plugs import usb
from openhtf.names import *


@plug(adb=usb.AdbPlug)
def TestADBPhase(test, adb):
    """
    Simple test to communicate with ADB
    """
    logging.debug('testADBPhase start!!!!')
    response = adb.Shell('ls')
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
