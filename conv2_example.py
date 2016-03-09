# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.signal import convolve2d as conv2

z = np.zeros((8, 8), dtype='float')
z[0:8:2, 0:8:2] = 1
kernal = np.array([[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]])
# print kernal
# z1=conv2(z,kernal)
# print z1

# z2=conv2(z,kernal,boundary='fill', mode='same')
# print z2
# print z2.shape

z2 = conv2(z, kernal, boundary='wrap', mode='same')
print z
print z2
