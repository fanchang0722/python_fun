import json
import matplotlib.pylab as plt

def parsed_result(parsed_json, key, sub_key):
    return parsed_json[key][sub_key]


file_name = r'/Users/fanchang/python_fun/DUT#_05_ff_result.json'
with open(file_name, 'r') as fp:
    result = fp.read()

parsed_json = json.loads(result)
key = 'blemishResults'
sub_keys = ['profile_Y_UL_LR', 'profile_Y_LL_UR', 'Optical_ctr_offset_pixels',
          'Optical_ctr_offset_radial_PXLS_PCT', 'R_B_ratio_ctr2corner_mean_variation',
          'R_B_ratio_ctr2corner_worst_variation', 'R_G_ratio_ctr2corner_mean_variation',
          'R_G_ratio_ctr2corner_worst_variation', 'G_B_ratio_ctr2corner_mean_variation',
          'G_B_ratio_ctr2corner_worst_variation', 'Gb_Gr_mean_ratio', 'R_G_mean_ratio',
          'G_B_mean_ratio', 'nDeadPixels', 'N_blemish_count']
for sub_key in sub_keys:
    print parsed_result(parsed_json, key, sub_key)

# Relative_Illumination = parsed_result(parsed_json, key, 'profile_Y_UL_LR')
# plt.plot(Relative_Illumination, '-o', lw=2)
# plt.grid(True)
# plt.show()