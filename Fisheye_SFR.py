# Copyright 2014 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# !/usr/bin/python
import os
import sys
import subprocess as sub
import logging
import json
import tempfile
import time
import math
import clifford
import Fisheye_spec
import GTAL
from clifford.names import *

conf.Declare('cam_exposure', description='camera exposure')
conf.Declare('testIni_name1', description='fishey1 ini name')
conf.Declare('testIni_name2', description='fishey2 ini name')
conf.Declare('spec_file', description='SFR spec file')
conf.Declare('upload_flag', description='upload to the server')
conf.Declare('source_location', description='DUT runtime path')
conf.Declare('file_name1', description='left 6Dof')
conf.Declare('file_name2', description='right 6Dof')
conf.Declare('dest_location', description='server path')
sys.path.append(os.path.dirname(str(conf.spec_file)))
# sys.path.append(os.path.dirname(str(conf.motor_file)))
# import motorController as motor

myGTAL = GTAL.initialize()
# vct = motor.motorController("/dev/ttyUSB0", 38400, 'VCT', False)


def motorinit():
    motor.ctrl_init(vct)


def motor2center():
    vct.XAxisMotion(0, 50, 2, 0)
    vct.YAxisMotion(0, 100, 2, 0)
    vct.RAxisMotion(1500, 2, 2, 1)
    # print 'move chart center 222222'


def motorPosRotate():
    vct.RAxisMotion(3000, 2, 2, 1)
    # print 'Positive rotation'


def motorNegRotate():
    vct.RAxisMotion(0, 2, 2, 1)
    # print 'Negative rotation'


def motorHome():
    vct.XAxisMotion(0, 50, 2, 0)
    vct.YAxisMotion(26000, 100, 2, 0)
    vct.RAxisMotion(1500, 2, 2, 1)
    # print 'back to loading'


def initialization(test_data):
    test_data.logger.info('Initialize adb server')
    sub.check_output(['adb', 'kill-server'])
    time.sleep(5)


def ff_id():
    result = sub.check_output(["adb", "devices"])
    time.sleep(3)
    sid = result.rsplit('\n')[-3].split('\t')[0]
    return sid


def stop_capture(test_data):
    result = sub.check_output(['adb', 'shell', 'stop', 'sensord'])
    test_data.logger.info('stop sensor capture')
    time.sleep(3)


def image_capture(test_data):
    # print ['adb', 'shell', 'tango_hal_test_cameras', '--batch', '--fishexp', str(conf.cam_exposure),
    #                            '--framecount', '2', 'FISHEYE', '10']
    result = sub.check_output(['adb', 'shell', 'tango_hal_test_cameras', '--batch', '--fishexp', str(conf.cam_exposure),
                               '--framecount', '2', 'FISHEYE', '10'])
    test_data.logger.info('image capture')


def get_left_6Dof(test_data):
    # print ['adb', 'pull', '/data/tango'+'/'+str(conf.file_name1), str(conf.dest_location)]
    result = sub.check_output(['adb', 'pull', '/data/tango'+'/'+str(conf.file_name1), str(conf.dest_location)])
    if os.path.exists(conf.dest_location[:-1] + str(conf.file_name1)):
        test_data.logger.info('\t adb pull successfully on left 6DoF image')


def get_right_6Dof(test_data):
    # print ['adb', 'pull', '/data/tango'+'/'+str(conf.file_name2), str(conf.dest_location)]
    result = sub.check_output(['adb', 'pull', '/data/tango'+'/'+str(conf.file_name2), str(conf.dest_location)])
    if os.path.exists(conf.dest_location[:-1] + str(conf.file_name2)):
        test_data.logger.info('\t adb pull successfully on right 6DoF image')


@measures(
    Measurement('Center1_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny4_H']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny4_H'])),
    Measurement('TopLeft1_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny4_H']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny4_H'])),
    Measurement('TopRight1_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny4_H']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny4_H'])),
    Measurement('BottomLeft1_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny4_H']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny4_H'])),
    Measurement('BottomRight1_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny4_H']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny4_H'])),
    Measurement('Center1_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny4_V']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny4_V'])),
    Measurement('TopLeft1_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny4_V']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny4_V'])),
    Measurement('TopRight1_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny4_V']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny4_V'])),
    Measurement('BottomLeft1_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny4_V']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny4_V'])),
    Measurement('BottomRight1_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny4_V']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny4_V'])),
    Measurement('Center1_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny2_H']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny2_H'])),
    Measurement('TopLeft1_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny2_H']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny2_H'])),
    Measurement('TopRight1_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny2_H']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny2_H'])),
    Measurement('BottomLeft1_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny2_H']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny2_H'])),
    Measurement('BottomRight1_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny2_H']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny2_H'])),
    Measurement('Center1_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny2_V']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny2_V'])),
    Measurement('TopLeft1_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny2_V']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny2_V'])),
    Measurement('TopRight1_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny2_V']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny2_V'])),
    Measurement('BottomLeft1_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny2_V']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny2_V'])),
    Measurement('BottomRight1_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny2_V']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny2_V']))
    )
@TestPhase(timeout_s=20)
def Fisheye1_SFR_test(test_data):
    testIni = str(conf.testIni_name1)
    paramOut = myGTAL.GTAL(testIni)
    test_data.measurements.Center1_SFR_Ny4_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][1], 4)
    test_data.measurements.TopLeft1_SFR_Ny4_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][3], 4)
    test_data.measurements.TopRight1_SFR_Ny4_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][5], 4)
    test_data.measurements.BottomLeft1_SFR_Ny4_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][7], 4)
    test_data.measurements.BottomRight1_SFR_Ny4_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][9], 4)
    test_data.measurements.Center1_SFR_Ny4_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][11], 4)
    test_data.measurements.TopLeft1_SFR_Ny4_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][13], 4)
    test_data.measurements.TopRight1_SFR_Ny4_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][15], 4)
    test_data.measurements.BottomLeft1_SFR_Ny4_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][17], 4)
    test_data.measurements.BottomRight1_SFR_Ny4_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][32][19], 4)
    test_data.measurements.Center1_SFR_Ny2_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][1], 4)
    test_data.measurements.TopLeft1_SFR_Ny2_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][3], 4)
    test_data.measurements.TopRight1_SFR_Ny2_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][5], 4)
    test_data.measurements.BottomLeft1_SFR_Ny2_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][7], 4)
    test_data.measurements.BottomRight1_SFR_Ny2_H = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][9], 4)
    test_data.measurements.Center1_SFR_Ny2_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][11], 4)
    test_data.measurements.TopLeft1_SFR_Ny2_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][13], 4)
    test_data.measurements.TopRight1_SFR_Ny2_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][15], 4)
    test_data.measurements.BottomLeft1_SFR_Ny2_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][17], 4)
    test_data.measurements.BottomRight1_SFR_Ny2_V = round(paramOut['Fisheye1_SFR']['paramout']['all_MTF'][64][19], 4)
    test_data.logger.info('Finish Fisheye1 SFR test')
    # header = ff_id()
    # filename = 'Fisheye_'+header + '_' + time.strftime("%Y%m%d_%H%M%S_left.raw")
    # print ['cp', conf.dest_location[:-1] + str(conf.file_name1),
    #                            os.path.join(str(conf.dest_location)[:-1], filename)]
    # result = sub.check_output(['cp', conf.dest_location[:-1] + str(conf.file_name1),
    #                            os.path.join(str(conf.dest_location)[:-1], filename)])
    #
    # test_data.AttachFromFile(os.path.join(str(conf.dest_location)[:-1], filename))

    test_data.logger.info('\t Upload image to the server')


@measures(
    Measurement('Center2_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny4_H']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny4_H'])),
    Measurement('TopLeft2_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny4_H']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny4_H'])),
    Measurement('TopRight2_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny4_H']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny4_H'])),
    Measurement('BottomLeft2_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny4_H']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny4_H'])),
    Measurement('BottomRight2_SFR_Ny4_H').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny4_H']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny4_H'])),
    Measurement('Center2_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny4_V']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny4_V'])),
    Measurement('TopLeft2_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny4_V']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny4_V'])),
    Measurement('TopRight2_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny4_V']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny4_V'])),
    Measurement('BottomLeft2_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny4_V']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny4_V'])),
    Measurement('BottomRight2_SFR_Ny4_V').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny4_V']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny4_V'])),
    Measurement('Center2_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny2_H']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny2_H'])),
    Measurement('TopLeft2_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny2_H']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny2_H'])),
    Measurement('TopRight2_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny2_H']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny2_H'])),
    Measurement('BottomLeft2_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny2_H']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny2_H'])),
    Measurement('BottomRight2_SFR_Ny2_H').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny2_H']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny2_H'])),
    Measurement('Center2_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['Center_SFR_Ny2_V']),
                                            float(Fisheye_spec.upper_spec['Center_SFR_Ny2_V'])),
    Measurement('TopLeft2_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['TopLeft_SFR_Ny2_V']),
                                             float(Fisheye_spec.upper_spec['TopLeft_SFR_Ny2_V'])),
    Measurement('TopRight2_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['TopRight_SFR_Ny2_V']),
                                              float(Fisheye_spec.upper_spec['TopRight_SFR_Ny2_V'])),
    Measurement('BottomLeft2_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['BottomLeft_SFR_Ny2_V']),
                                                float(Fisheye_spec.upper_spec['BottomLeft_SFR_Ny2_V'])),
    Measurement('BottomRight2_SFR_Ny2_V').InRange(float(Fisheye_spec.lower_spec['BottomRight_SFR_Ny2_V']),
                                                 float(Fisheye_spec.upper_spec['BottomRight_SFR_Ny2_V']))
)
@TestPhase(timeout_s=20)
def Fisheye2_SFR_test(test_data):
    testIni = str(conf.testIni_name2)
    paramOut = myGTAL.GTAL(testIni)
    test_data.measurements.Center2_SFR_Ny4_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][1], 4)
    test_data.measurements.TopLeft2_SFR_Ny4_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][3], 4)
    test_data.measurements.TopRight2_SFR_Ny4_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][5], 4)
    test_data.measurements.BottomLeft2_SFR_Ny4_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][7], 4)
    test_data.measurements.BottomRight2_SFR_Ny4_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][9], 4)
    test_data.measurements.Center2_SFR_Ny4_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][11], 4)
    test_data.measurements.TopLeft2_SFR_Ny4_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][13], 4)
    test_data.measurements.TopRight2_SFR_Ny4_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][15], 4)
    test_data.measurements.BottomLeft2_SFR_Ny4_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][17], 4)
    test_data.measurements.BottomRight2_SFR_Ny4_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][32][19], 4)
    test_data.measurements.Center2_SFR_Ny2_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][1], 4)
    test_data.measurements.TopLeft2_SFR_Ny2_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][3], 4)
    test_data.measurements.TopRight2_SFR_Ny2_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][5], 4)
    test_data.measurements.BottomLeft2_SFR_Ny2_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][7], 4)
    test_data.measurements.BottomRight2_SFR_Ny2_H = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][9], 4)
    test_data.measurements.Center2_SFR_Ny2_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][11], 4)
    test_data.measurements.TopLeft2_SFR_Ny2_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][13], 4)
    test_data.measurements.TopRight2_SFR_Ny2_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][15], 4)
    test_data.measurements.BottomLeft2_SFR_Ny2_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][17], 4)
    test_data.measurements.BottomRight2_SFR_Ny2_V = round(paramOut['Fisheye2_SFR']['paramout']['all_MTF'][64][19], 4)
    # test_data.logger.info('Finish Fisheye2 SFR test')
    # header = ff_id()
    # filename = 'Fisheye_'+header + '_' + time.strftime("%Y%m%d_%H%M%S_right.raw")
    # result = sub.check_output(['cp', conf.dest_location[:-1] + str(conf.file_name2),
    #                            os.path.join(str(conf.dest_location)[:-1], filename)])
    #
    # test_data.AttachFromFile(os.path.join(str(conf.dest_location)[:-1], filename))
    test_data.logger.info('\t Upload image to the server')

def delete_raw():
    # print ['rm', str(conf.dest_location)[:-1]+'*.raw']
    sub.check_output(['rm', str(conf.dest_location)[:-1] + str(conf.file_name1)])
    sub.check_output(['rm', str(conf.dest_location)[:-1] + str(conf.file_name2)])

def teardown(test_data):
    test_data.logger.info('Prepare for next one')

# Phases = [motorinit, motorHome, motor2center, motorPosRotate,
#           initialization, stop_capture, image_capture, get_left_6Dof, Fisheye1_SFR_test,
#           motorNegRotate, image_capture, get_right_6Dof, Fisheye2_SFR_test, delete_raw, motorHome]
Phases = [Fisheye2_SFR_test]
# Phases = [motorinit, motorHome, motor2center, motorPosRotate, motorNegRotate, motorHome]
if __name__ == '__main__':
    test = clifford.Test(*Phases, test_name='Fisheye_SFR_test', test_description='SFR',
                         test_version='cam_SFR_1.0.4')

    """ upload the test result to data server and keep a local copy"""
    # test.AddOutputCallback(UploadResultJSON(
    #   './%(dut_id)s.%(start_time_millis)s.json', indent=4))
    if float(conf.upload_flag):
        test.AddOutputCallback(UploadResultJSON())

    """ upload test result to cm server"""
    # test.AddOutputCallback(UploadResultCM())
    # add teardown function (destructor), which is guaranteed to be called at last.
    test.Configure(teardown_function=teardown)
    test.StartExecution(test)
    # test.StartExecution(test, test_start=ff_id)
