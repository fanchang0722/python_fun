import os
import GTAL_EVT

myGTAL = GTAL_EVT.initialize()
testini=r'c:/Users/fanchang/Documents/MATLAB/test_B4S4_MI.ini'
paramOut = myGTAL.GTAL_EVT(testini)

print paramOut.keys()
print paramOut['version']
print paramOut['Front_Light']['paramout']['RI']
print (5 * '=' + "done" + 5 * '=')

