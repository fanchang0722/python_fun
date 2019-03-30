import os, sys, json, time

def parsed_result(parsed_json, key, sub_key):
    return parsed_json[key][sub_key]

directory = r'/Users/fanchang/Desktop/Phoenix/P2/All Json Files'
fileList = os.listdir(directory)
outfile = r'/Users/fanchang/Downloads/P2_all_OQC_SFR.csv'
fout = open(outfile, 'w')
header ='FF_SID,IH_H_0,IH_H_1,IH_H_2,IH_H_3,IH_H_4,IH_H_5,IH_H_6,IH_H_7,IH_H_8,IH_H_9,IH_H_10,IH_H_11,' \
        'IH_V_0,IH_V_1,IH_V_2,IH_V_3,IH_V_4,IH_V_5,IH_V_6,IH_V_7,IH_V_8,IH_V_9,IH_V_10,IH_V_11,' \
        'SFR_H_0,SFR_H_1,SFR_H_2,SFR_H_3,SFR_H_4,SFR_H_5,SFR_H_6,SFR_H_7,SFR_H_8,SFR_H_9,SFR_H_10,SFR_H_11,' \
        'SFR_V_0,' \
        'SFR_V_1,' \
        'SFR_V_2,' \
        'SFR_V_3,' \
        'SFR_V_4,' \
        'SFR_V_5,' \
        'SFR_V_6,' \
        'SFR_V_7,' \
        'SFR_V_8,' \
        'SFR_V_9,' \
        'SFR_V_10,' \
        'SFR_V_11\n' \

fout.write(header)
count = 0
for filename in fileList:
    if filename.startswith('sfrplus_0') and os.path.getsize(os.path.join(directory, filename)) > 0:
        count += 1
        temp = ''
        print filename
        temp += filename[8:-5]+','
        with open(os.path.join(directory, filename), 'r') as fp:
            result = fp.read()
        parsed_json = json.loads(result)

        key = 'sfrplusResults'
        sub_keys = {'IH': 'distance_Pct',
                    'SFR_Ny4': 'secondary_1_results',
                    'Field_of_View': 'FieldofView_DiagHV_degrees',
                    'Color_Aberration': 'CA_areaPxls',
                    'Tilt_overall_H': 'H_conv_angle_degrees',
                    'Tilt_overall_V': 'V_conv_angle_degrees',
                    'Rotation': 'rotationDegrees',
                    'SMIA_distortion': 'SMIA_TV_Distortion_Pct'}
        result = parsed_result(parsed_json, key, sub_keys['IH'])+parsed_result(parsed_json, key, sub_keys['SFR_Ny4'])

        for element in range(len(result)):
            temp += str(result[element])+','
        fout.write(temp[:-1])
        fout.write('\n')
            # time.sleep(.2)
        # for sub_key in sub_keys.keys():
        #     # print sub_key
        #     # sub_key=parsed_json(parsed_json, key, sub_keys[sub_key])
        #     print sub_key
        #     print parsed_result(parsed_json, key, sub_keys[sub_key])
        # fp.writelines(temp)

fout.close()
print 'count is %d' % count,
