# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:35:07 2016

@author: fanchang
"""

import matplotlib.pylab as plt
import numpy as np

fid = open('/Users/fanchang/Desktop/img1.raw10', 'rb')
data = fid.read()
fid.close()
img = np.reshape(data, (3328, 2448))
plt.show(img)
