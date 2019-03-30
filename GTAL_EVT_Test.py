import os
import GTAL_EVT

myGTAL = GTAL_EVT.initialize()
testini=r'c:/Users/fanchang/Documents/MATLAB/test_B4S4_MI.ini'
paramOut = myGTAL.GTAL_EVT(testini)

print paramOut.keys()
print paramOut['version']
print paramOut['Front_Light']['paramout']['RI']
print (5 * '=' + "done" + 5 * '=')


# folder = r'C:\Users\fanchang\CommonUtils\libGTAL_B1\Common\temp'
# filelists = os.listdir(folder)

# for filename in filelists:
# 	if filename.endswith('ini'):
# 		print (os.path.join(folder, filename))
# 		paramOut = myGTAL.GTAL_EVT(os.path.join(folder, filename))
# 		print (paramOut)