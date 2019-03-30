import json
import matplotlib.pylab as plt

def parsed_result(parsed_json, key, sub_key):
    return parsed_json[key][sub_key]


file_name = r'/Users/fanchang/python_fun/DUT#_05_dar_result.json'
with open(file_name, 'r') as fp:
    result = fp.read()

parsed_json = json.loads(result)
key = 'blemishResults'
sub_keys = ['R_mean', 'Gb_mean', 'Gr_mean', 'B_mean',
            'R_Std', 'Gb_Std', 'Gr_Std', 'B_Std',
            'nHotPixels', 'N_blemish_count']
for sub_key in sub_keys:
    print parsed_result(parsed_json, key, sub_key)

plt.plot(parsed_result(parsed_json, key, 'R_mean'), '-o', lw=2)