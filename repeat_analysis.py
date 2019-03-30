import json
import os
import matplotlib.pylab as plt
import numpy as np
# import seaborn as sns


def parsed_result(parsed_json, key, sub_key):
    return parsed_json[key][sub_key]


def cpk(data, usl, lsl, round_digit=3):
    mu = round(np.mean(data), round_digit)
    sig = round(np.std(data), round_digit)
    cp = round((usl-lsl)/(6.0*sig), round_digit)
    cp_upper = round((usl-mu)/(3.0*sig), round_digit)
    cp_lower = round((mu-lsl)/(3.0*sig), round_digit)
    cpk = round(np.min([cp_upper, cp_lower]), round_digit)
    return [mu,sig, cp, cp_upper, cp_lower, cpk]

directory = r'/Users/fanchang/Desktop/camera_test_result/SFR/'
os.chdir(directory)
rotation_record = []
sfr_record = []
for filename in os.listdir(os.getcwd()):
    print os.path.join(directory, filename)
    with open(os.path.join(directory, filename), 'r') as fp:
        result = fp.read()
    parsed_json = json.loads(result)
    key = 'sfrplusResults'
    sub_keys = 'rotationDegrees'
    rotation_record.append(parsed_result(parsed_json, key, sub_keys)[0])
    sub_keys = 'secondary_1_results'
    sfr_record.append(parsed_result(parsed_json, key, sub_keys))
rotation = np.array(rotation_record)
print cpk(rotation, 2, -2, 4)

sfr = np.array(sfr_record)
print cpk(sfr[:,0], 1, 0.37, 4)
print cpk(sfr[:,1], 1, 0.37, 4)
print cpk(sfr[:,2], 1, 0.37, 4)
print cpk(sfr[:,4], 1, 0.37, 4)
plt.figure(figsize=[8*1.2,6*1.2])
#plt.ylim([0.3,.8])
#plt.plot(np.transpose(sfr),'o')
plt.boxplot(sfr)
#plt.boxplot(rotation_record)
plt.show()
