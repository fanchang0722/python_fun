# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 09:22:04 2016

@author: fanchang
"""
import os

import matplotlib.pylab as plt
import numpy as np

folder = r'/Users/fanchang/python_fun/Numpy_beginner_example_code'
bhp = np.loadtxt(os.path.join(folder, 'Chapter4/BHP.csv'),
                 delimiter=',', usecols=(6,), unpack=True)
vale = np.loadtxt(os.path.join(folder, 'Chapter4/VALE.csv'),
                  delimiter=',', usecols=(6,), unpack=True)
t = np.arange(len(bhp))
poly = np.polyfit(t, (bhp - vale), 3)
print np.polyder(poly)
print np.roots(np.polyder(poly))
print np.polyval(poly, [7, 24])
print np.polyval(poly, np.roots(np.polyder(poly)))
plt.plot(t, (bhp - vale), '--o', t, np.polyval(poly, t), '-r', lw=2)
plt.grid(True)
plt.show()
