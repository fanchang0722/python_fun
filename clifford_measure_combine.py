"""
Script to combine GRR phase measurement
"""
import os
folder = r'C:\Users\fanchang\python_fun\G501_COMBO3_N1'
# print folder.split('/')[-1]
keys = range(1, 20, 1)
folderNames = os.listdir(folder)

for idx in keys:
    count = 0
    if idx > 9:
        endstring = str(idx)
    else:
        endstring = '0'+str(idx)
    fout = open(folder.split('/')[-1]+'_phase_'+endstring+'_out.csv', 'w')
    print folder.split('/')[-1]+'_phase_'+endstring+'_out.csv'
    for fileName in folderNames:
        if fileName.endswith(endstring+'.csv'):
            if os.path.exists(os.path.join(folder, fileName)):
                # print fileName
                fp = open(os.path.join(folder, fileName), 'r')
                header = fp.readline().rstrip('\r\n')
                result = fp.readline().rstrip('\r\n')
                # print header
                print result
                fp.close()
                if count == 0:
                    fout.writelines(header+'\r')
                    fout.writelines(result+'\r')
                else:
                    fout.writelines(result+'\r')
                count += 1
    fout.close()
