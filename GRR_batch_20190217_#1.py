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

"""
Script to parse clifford json measurement
"""
import json
import os
# import time


def grrparse(folderin, folderout):

	if not os.path.exists(os.path.join(folderout, 'temp')):
		os.mkdir(os.path.join(folderout, 'temp'))
	station = folderin.split('\\')[-1]  # Get station name

	# Create folder for each GRR station
	newfolder = os.path.join(folderout, station)
	if not os.path.exists(newfolder):
		os.makedirs(newfolder)

	# Get Operator folder
	subfolders = os.listdir(folderin)
	for subfolder in subfolders:
		if not subfolder.startswith('.'):
			op = subfolder
			count = 0
			meas = 0
			for fileName in os.listdir(os.path.join(folderin, subfolder)):
				if fileName.endswith('json'):
					meas += 1
					count += 1
					print(fileName)
					# sn is serial number of phone
					sn = fileName.split('_')[1]
					with open(os.path.join(os.path.join(folderin, subfolder), fileName), 'r') as fp:
						result = fp.read()
						# time.sleep(5)
					parsed_json = json.loads(result)
					key = 'phases'
					# subkey = 'measurements'
					index = 1

					for idx in range(len(parsed_json[key])):
						outname = os.path.join(os.path.join(folderout, 'temp'), sn + ("_%s_measurement%d_%02d.csv" % (op, meas, index)))
						fp = open(outname, 'w')
						if parsed_json[key][idx]['measurements']:
							temp = 'Station,sn,Operator,Phase,'
							temp2 = station + ',' + fileName.split('_')[1] + ',' + op + ',' + parsed_json[key][idx]['name'] + ','
							for subkey in parsed_json[key][idx]['measurements'].keys():
								temp += str(parsed_json[key][idx]['measurements'][subkey].values()[2]) + ','
								temp2 += str(parsed_json[key][idx]['measurements'][subkey].values()[1]) + ','
							index += 1
							fp.writelines(temp[:-1] + '\n')
							fp.writelines(temp2[:-1] + '\n')
						fp.close()

	folder = os.path.join(folderout, 'temp')
	keys = range(1, 30, 1)
	foldernames = os.listdir(folder)

	for idx in keys:
		count = 0
		if idx > 9:
			endstring = str(idx)
		else:
			endstring = '0' + str(idx)
		fout = open(folderin.split('\\')[-1] + '_phase_' + endstring + '_out.csv', 'w')
		print(folderin.split('\\')[-1] + '_phase_' + endstring + '_out.csv')
		for fileName in foldernames:
			if fileName.endswith(endstring + '.csv'):
				if os.path.exists(os.path.join(folder, fileName)):
					# print os.path.join(folder, fileName)
					fp = open(os.path.join(folder, fileName), 'r')
					header = fp.readline().rstrip('\n')
					result = fp.readline().rstrip('\n')
					fp.close()
					if count == 0:
						fout.writelines(header + '\n')
						fout.writelines(result + '\n')
					else:
						fout.writelines(result + '\n')
					count += 1
					os.remove(os.path.join(folder, fileName))
		fout.close()
		if os.path.getsize(folderin.split('\\')[-1] + '_phase_' + endstring + '_out.csv') <= 2000:
			os.remove(os.path.join(os.getcwd(), folderin.split('\\')[-1] + '_phase_' + endstring + '_out.csv'))


def main():
	folderin = r"C:\Users\fanchang\Desktop\COMBO3_GRR\G501_COMBO3_N3"
	folderout = r'C:\Users\fanchang\Downloads\temp'
	grrparse(folderin, folderout)


if __name__ == '__main__':
	main()