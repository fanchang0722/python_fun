import pandas as pd
import sys
import os
import seaborn
import matplotlib.pylab as plt


def camerastation_daily(filename):
    fid = open(filename, 'r')
    SNDict = dict()
    passSN = dict()
    header = fid.readline().rstrip('\r\n')
    count = 0
    for line in fid:
        temp = line.rstrip('\r\n').split(',')
        count += 1
        SN = temp[2]
#         status = temp[4]
        status = temp[5]
        if SN not in SNDict:
            SNDict[SN] = 1
        else:
            SNDict[SN] += 1
        if status == 'PASS':
                passSN[SN] = 1
    fid.close()
    firstPass = {key:value for key, value in SNDict.items() if value == 1}
    secondPass = {key:value for key, value in SNDict.items() if value == 2}
    thirdPass = {key:value for key, value in SNDict.items() if value == 3}
    [keys_1st_pass, keys_1st_nopass] = intersection2dict(firstPass, passSN)
    [keys_2nd_pass, keys_2nd_nopass] = intersection2dict(secondPass, passSN)
    [keys_3rd_pass, keys_3rd_nopass] = intersection2dict(thirdPass, passSN)
    firstpass_yield = 0
    secondpass_yield = 0
    retest_rate = 0
    if len(passSN):
        firstpass_yield = 100.*len(keys_1st_pass)/len(passSN)
        secondpass_yield = 100.*(len(keys_1st_pass)+len(keys_2nd_pass))/len(passSN)
        retest_rate = 100.*(count-len(SNDict))/len(SNDict)
    # print count
    # print len(SNDict)
    # print len(passSN)
    # print len(keys_1st_pass)
    # print len(keys_2nd_pass)
    # print len(keys_3rd_pass)
    # print 100.*len(keys_1st_pass)/len(passSN)
    # print 100.*(count-len(SNDict))/len(SNDict)
    # print '\t{0:.4f}%'.format(firstpass_yield)
    # print '\t{0:.4f}%'.format(secondpass_yield)
    # print '\t{0:.4f}%'.format(retest_rate)
    return [count, firstpass_yield, secondpass_yield, retest_rate, SNDict, passSN, keys_1st_pass, keys_1st_nopass,
            keys_2nd_pass, keys_2nd_nopass, keys_3rd_pass, keys_3rd_nopass]



def intersection2dict(dict1, dict2):
    """find the intersection of two dictionaries"""
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    intersection = keys1 & keys2
    difference = keys1 ^ intersection
    return [intersection, difference]

# filename = r'c:/Users/fanchang/Desktop/B1C1_combo1_20181111_20181117083606.csv'
filename = r'c:/Users/fanchang/Desktop/C2_combo1_20181111_20181127090420.csv'
df = pd.read_csv(filename)
# print df.head(5)
# print len(sorted(df.station_id.unique()))
# print len(sorted(df.china_date.unique()))
fid = open('C2_Combo1_final_result.csv', 'w')
fid.writelines('station,chinadate,1stPass,2ndPass,retest,count,#SN,#Pass\r')
for station in sorted(df.station_id.unique()):
	for chinadate in sorted(df.china_date.unique()):
		newdf = df[df.station_id == station]
		Newdf = newdf[newdf.china_date == chinadate]
		# print len(Newdf)
		if len(Newdf):
			Newdf.to_csv('Newfile.csv', index=False)
			[count, firstpass_yield, secondpass_yield, retest_rate, SNDict, passSN, keys_1st_pass, keys_1st_nopass,
			 keys_2nd_pass, keys_2nd_nopass, keys_3rd_pass, keys_3rd_nopass] = camerastation_daily('Newfile.csv')
			print station, chinadate, firstpass_yield, secondpass_yield, retest_rate, len(SNDict), len(passSN)
			fid.writelines(str(station)+','+str(chinadate)+','+str(firstpass_yield)+','+str(secondpass_yield)+','+str(retest_rate)+','+str(count)+','+str(len(SNDict))+','+str(len(passSN))+'\r')
fid.close()
print '----- done -----'
