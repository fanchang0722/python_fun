#  Copyright 2014 Google Inc. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns


def daily_plot(filename, image_path):
	df = pd.read_csv(filename)
	# Stripe out the month and day
	new = df['china_time'].str.split("-", n=1, expand=True)
	df['year'] = new[0]
	df['date'] = new[1]
	# Generate plot
	# plt.figure(figsize=(20, 5))
	# sns.countplot(x='date', data=df, hue='station_id')
	# plt.savefig(image_path, dpi=240)
	count = 1
	for year in df.year.unique():
		temp = pd.DataFrame()
		plt.figure(figsize=(20, 5))
		temp = df[df['year'] == year]
		sns.countplot(x='date', data=temp, hue='station_id')
		plt.savefig(str(year)+'_'+image_path, dpi=240)
		count += 1


def main():
	folder = r'c:/Users/fanchang/Downloads'
	filename = r'C2F2_station_20190324100658.csv'
	filename = os.path.join(folder, filename)
	image_path = r'COMBO2_EVT.png'
	daily_plot(filename, image_path)
	print('done')


if __name__ == '__main__':
	main()
