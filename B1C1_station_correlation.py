import numpy as np
import scipy as sp
import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd
import os


folder=r'C:\Users\fanchang\Desktop\G03'
foldername =['G03_COMBO1_N2', 'G03_COMBO1_N3', 'G03_COMBO1_N4', 'G03_COMBO1_N5']
folderstring = 'processed'
leadname = 'G03_COMBO1_N1'
print os.path.join(os.path.join(os.path.join(folder, leadname), folderstring), 'G03_COMBO1_N1_phase_02_out.csv')
df = pd.read_csv(os.path.join(os.path.join(os.path.join(folder, leadname), folderstring), 'G03_COMBO1_N1_phase_02_out.csv'))

for item1 in foldername:
    subfolder = os.path.join(os.path.join(folder, item1), folderstring)
    print subfolder
    for item2 in os.listdir(subfolder):
        if item2.endswith('phase_02_out.csv'):
            temp2 = pd.read_csv(os.path.join(subfolder, item2))
            df = df.append(temp2)