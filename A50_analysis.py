# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 00:09:25 2017

@author: fanchang
"""

import os

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from scipy import stats

file_loc = r'/Users/fanchang/Desktop/A50/LiteOn_module'
file_name = r'P1_13pc_liteon.csv'
df_module = pd.read_csv(os.path.join(file_loc, file_name))
print (df_module.head(5))

file_loc = r'/Users/fanchang/Desktop/A50/IQC_correlation'
file_name = r'13pcs_tracking_focus_iq_off.csv'
df_IQC = pd.read_csv(os.path.join(file_loc, file_name))
print (df_IQC.head(5))

df_module_IQC = df_module.merge(df_IQC, left_on='SeqNO', right_on='SN', how='inner')

x = np.array(df_module_IQC['CT'])
y = np.array(df_module_IQC['V_SFR@0.125C/P_C'])
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
p = np.poly1d([slope, intercept])
print ("R-squared:", r_value ** 2)
print ("MSE:", std_err)

plt.figure(figsize=[12, 9])
plt.plot(df_module_IQC['CT'], df_module_IQC['V_SFR@0.125C/P_C'], 'o', markersize=8)
plt.plot(np.sort(df_module_IQC['CT']), p(np.sort(df_module_IQC['CT'])), '-', lw=2)
plt.grid(True)
plt.xlabel('Module center SFR')
plt.ylabel('IQC center SFR')

cam_fatp = pd.read_csv(r'/Users/fanchang/Downloads/report_0109day/report_0109day/check_focus_pass_20170109.csv')
cam_fatp.head(5)
plt.figure(figsize=[12, 9])
plt.hist([cam_fatp['V_SFR@0.125C/P_C'], cam_fatp['H_SFR@0.125C/P_C']])
