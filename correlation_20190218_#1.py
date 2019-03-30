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
import numpy as np
import scipy as sp
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

df1 = pd.read_csv(r"C:\Users\fanchang\python_fun\G501_COMBO2_N1_phase_13_out.csv")
df2 = pd.read_csv(r"C:\Users\fanchang\python_fun\G501_COMBO2_N2_phase_13_out.csv")
df3 = pd.read_csv(r"C:\Users\fanchang\python_fun\G501_COMBO2_N3_phase_13_out.csv")
df4 = pd.read_csv(r"C:\Users\fanchang\python_fun\G501_COMBO2_N4_phase_13_out.csv")
df = pd.concat([df1, df2, df3, df4])
dfgroup = df.groupby([df['Station'], df['SN']])
newdf = dfgroup.mean().reset_index()
cols = newdf.columns
newdf1 = newdf[newdf['Station'] == 'G501_COMBO2_N1']
newdf2 = newdf[newdf['Station'] == 'G501_COMBO2_N2']
newdf3 = newdf[newdf['Station'] == 'G501_COMBO2_N3']
newdf4 = newdf[newdf['Station'] == 'G501_COMBO2_N4']
cols = newdf1.columns
Newdf = newdf1[['SN']]
for idx in range(len(Newdf)):
	# Newdf.loc[idx, newdf1['Station'].drop_duplicates().values[0] + '_' + cols[2]] = newdf1[cols[2]].values[idx]
	# Newdf.loc[idx, newdf2['Station'].drop_duplicates().values[0] + '_' + cols[2]] = newdf2[cols[2]].values[idx]
	# Newdf.loc[idx, newdf3['Station'].drop_duplicates().values[0] + '_' + cols[2]] = newdf3[cols[2]].values[idx]
	# Newdf.loc[idx, newdf4['Station'].drop_duplicates().values[0] + '_' + cols[2]] = newdf4[cols[2]].values[idx]
	Newdf.loc[idx, newdf1['Station'].drop_duplicates().values[0]] = newdf1[cols[2]].values[idx]
	Newdf.loc[idx, newdf2['Station'].drop_duplicates().values[0]] = newdf2[cols[2]].values[idx]
	Newdf.loc[idx, newdf3['Station'].drop_duplicates().values[0]] = newdf3[cols[2]].values[idx]
	Newdf.loc[idx, newdf4['Station'].drop_duplicates().values[0]] = newdf4[cols[2]].values[idx]
# print(Newdf)
# plt.figure(figsize=(16, 10))
g = sns.pairplot(Newdf, kind="reg")
g.fig.suptitle('60%IH_SFR')
plt.show()