#  Copyright 2014 Google Inc. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import matplotlib.pylab as plt
import C2F2_MFOV_Raw
import C2F2_IR_raw
import matplotlib
import cv2

myMFOV = C2F2_MFOV_Raw.initialize()  # type: matlab_object
filename = r'C:\Users\fanchang\Desktop\camera_clifford\ImageFilename.raw'
fout = r'test.png'
result = myMFOV.C2F2_MFOV_Raw(filename, fout)
myMFOV.terminate()
print(result['logic'])

# myIR = C2F2_IR_raw.initialize()
# filename = r'C:\Users\fanchang\Desktop\camera_clifford\ir0.raw'
# fout = r'test2.png'
# result = myIR.C2F2_IR_raw(filename, fout)
# myIR.terminate()
# print(result['logic'])

print(matplotlib.__version__)
print(cv2.__version__)
