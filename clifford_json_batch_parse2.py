"""
Script to parse clifford json measurement
"""
#!/anaconda/bin/python
import json
import os
import subprocess as sub
import time
#
# GRRFolder = r'GRR_B1_OIS#3'
# print(GRRFolder)
# folderName = r'Users/fanchang/Desktop/B1C1EVT/B1/GRR_B1_OIS'
# folderName = os.path.join(folderName, GRRFolder)
# print(folderName)

folderName = r'C:\Users\fanchang\Desktop\COMBO3_GRR\G501_COMBO3_N1'
# print(folderName)

station = folderName.split('\\')[-1]  # Get station name
print(station)
# print os.path.join(r'C:\Users\fanchang\python_fun', station)

# Create folder for each GRR station
newfolder = os.path.join(r'C:\Users\fanchang\python_fun', station)
if not os.path.exists(newfolder):
    os.makedirs(newfolder)


# Get Operator folder
subfolders = os.listdir(folderName)
for subfolder in subfolders:
    if not subfolder.startswith('.'):
        op = subfolder
        # print op
        count = 0
        meas = 0
        for fileName in os.listdir(os.path.join(folderName, subfolder)):
            # print fileName
            if fileName.endswith('json'):
                meas += 1
                count += 1
                print(fileName)
                # time.sleep(0.2)
                # print fileName.split('_')[1]
                SN = fileName.split('_')[1]
                # print SN
                with open(os.path.join(os.path.join(folderName, subfolder), fileName), 'r') as fp:
                    result = fp.read()

                parsed_json = json.loads(result)
                key = 'phases'
                subkey = 'measurements'
                index = 1
                for idx in range(len(parsed_json[key])):
                    # print str(idx) + '--->'
                    # print parsed_json[key][idx]
                    outName = os.path.join(r'C:\Users\fanchang\python_fun', station,
                                           SN+("_%s_measurement%d_%02d.csv" % (op, meas, index)))
                    # print(outName)
                    # time.sleep(0.2)
                    fp = open(outName, 'w')
                    # fp = open(SN+("_%s_measurement_%02d.csv" % (op, index)), 'w')
                    if parsed_json[key][idx]['measurements']:
                        # print parsed_json[key][idx]['measurements'].keys()
                        temp = 'Station,SN,Operator,'
                        temp2 = station + ',' + fileName.split('_')[1] + ',' + op + ','
                        for subkey in parsed_json[key][idx]['measurements'].keys():
                            # print parsed_json[key][idx]['measurements'][subkey]
                            # print type(parsed_json[key][idx]['measurements'][subkey].values())
                            temp += str(parsed_json[key][idx]['measurements'][subkey].values()[2]) + ','
                            temp2 += str(parsed_json[key][idx]['measurements'][subkey].values()[1]) + ','
                        index += 1
                    # print parsed_json[key][idx]['measurements'].values()
                    #     print temp
                    #     print temp2
                        fp.writelines(temp + '\r\n')
                        fp.writelines(temp2 + '\r\n')
                    fp.close()

            # print count
        # print fp
        # sub.call(['mv', '*.csv', os.path.join(r'/Users/fanchang/python_fun', station)])
