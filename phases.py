"""Camera MTF tester for Phoenix."""
import time

from openhtf.names import *
from openhtf import plugs
from openhtf.plugs import usb
from openhtf import conf
import glassdut.openhtf_phases as ph
import example_plug
"""
How to launch tester.
python ./phases.py --config ./phases.yaml
"""


def module_img_capture(test):
    print 1
#    test.logger.info('Press plate against DUT then press enter')
#    test.logger.info('Enter was pressed, continue....')


def module_img_analysis(test):
    print 2
#    test.logger.info('Move plate away from DUT then press enter')
#    test.logger.info('Enter was pressed, continue....')


def Sleepphase(test):
    time.sleep(1)
#    new = prompts.DisplayPrompt('What\'s new?')
#    print 'Here\'s what\'s new: %s' % new


PHASES = [
    module_img_capture,
    module_img_analysis,
    Sleepphase,
]

  
if __name__ == '__main__':
    test = openhtf.Test(*PHASES)
    test.AddOutputCallback(OutputToJSON('./%(dut_id)s.%(start_time_millis)s', indent=4))
    test.Execute(test_start=triggers.PromptForTestStart())
    print "phases test completed"
