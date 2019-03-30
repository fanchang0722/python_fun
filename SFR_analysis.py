import json
import matplotlib.pylab as plt

def parsed_result(parsed_json, key, sub_key):
    return parsed_json[key][sub_key]

file_name=r'/Users/fanchang/Result/JSON/BSJ1P0M916232719_20160610-222343_SFR_Pos_Rel.json'
with open(file_name, 'r') as fp:
    result = fp.read()

parsed_json = json.loads(result)
# print type(parsed_json)
# print parsed_json['sfrplusResults'].keys()
key = 'sfrplusResults'
sub_keys = ['distance_Pct', 'secondary_1_results', 'FieldofView_DiagHV_degrees',
          'CA_areaPxls', 'H_conv_angle_degrees', 'V_conv_angle_degrees',
            'rotationDegrees', 'SMIA_TV_Distortion_Pct']
# for sub_key in sub_keys:
#     print parsed_result(parsed_json, key, sub_key)

IH = parsed_json['sfrplusResults']['distance_Pct']
SFR_Ny4 = parsed_json['sfrplusResults']['secondary_1_results']
print IH[:12]
print SFR_Ny4[:12]
Field_of_View = parsed_json['sfrplusResults']['FieldofView_DiagHV_degrees']
Color_Aberration = parsed_json['sfrplusResults']['CA_areaPxls']
Tilt_Lens2Snsr = [round(max(SFR_Ny4[8:12])-min(SFR_Ny4[8:12]), 5),
                  round(max(SFR_Ny4[20:])-min(SFR_Ny4[20:]), 5)]
Tilt_overall = [parsed_json['sfrplusResults']['H_conv_angle_degrees'][0],
              parsed_json['sfrplusResults']['V_conv_angle_degrees'][0]]

Rotation = parsed_json['sfrplusResults']['rotationDegrees']
SMIA_distortion = parsed_json['sfrplusResults']['SMIA_TV_Distortion_Pct']
# print len(SFR_Ny4)
# print len(Field_of_View)
# print 1
# # print len(max(Color_Aberration))
# print len(Tilt_Lens2Snsr)
# print len(Tilt_overall)
# print len(Rotation)
# print len(SMIA_distortion)
# print [max(Color_Aberration)]
output_after = IH+SFR_Ny4+Field_of_View+[max(Color_Aberration)]+Tilt_Lens2Snsr+Tilt_overall+Rotation+SMIA_distortion
# print [IH, SFR_Ny4, Field_of_View, Color_Aberration,Tilt_Lens2Snsr, Tilt_overall, Rotation, SMIA_distortion]
# print 'Image Height %s' % IH
# print 'SFR %s' % SFR_Ny4
#
# print 'Diagonal Field of View %.2f' % Field_of_View[0]
# print 'Horizontal Field of View %.2f' % Field_of_View[1]
# print 'Vertical Field of View %.2f' % Field_of_View[2]
# print 'Color_Aberration %.2f' % max(Color_Aberration)
# print 'Tilt_overall %s' % Tilt_Lens2Snsr
# print 'Tilt_overall %s' % Tilt_overall
# print 'Rotation %.2f' % Rotation[0]
# print 'SMIA distortion %.2f' % SMIA_distortion[0]
plt.plot(IH[0:12], SFR_Ny4[0:12], 'go', lw=3)
# plt.plot(IH[12:], SFR_Ny4[12:], 'rx', lw=3)
plt.grid()
# plt.show()

file_name=r'/Users/fanchang/Result/JSON/BSJ1P0M916232719_20160608-195639_SFR_Pos.json'
with open(file_name, 'r') as fp:
    result = fp.read()

parsed_json = json.loads(result)
# print type(parsed_json)
# print parsed_json['sfrplusResults'].keys()
key = 'sfrplusResults'
sub_keys = ['distance_Pct', 'secondary_1_results', 'FieldofView_DiagHV_degrees',
          'CA_areaPxls', 'H_conv_angle_degrees', 'V_conv_angle_degrees',
            'rotationDegrees', 'SMIA_TV_Distortion_Pct']
# for sub_key in sub_keys:
#     print parsed_result(parsed_json, key, sub_key)

IH = parsed_json['sfrplusResults']['distance_Pct']
SFR_Ny4 = parsed_json['sfrplusResults']['secondary_1_results']
print IH[:12]
print SFR_Ny4[:12]
Field_of_View = parsed_json['sfrplusResults']['FieldofView_DiagHV_degrees']
Color_Aberration = parsed_json['sfrplusResults']['CA_areaPxls']
Tilt_Lens2Snsr = [round(max(SFR_Ny4[8:12])-min(SFR_Ny4[8:12]), 5),
                  round(max(SFR_Ny4[20:])-min(SFR_Ny4[20:]), 5)]
Tilt_overall = [parsed_json['sfrplusResults']['H_conv_angle_degrees'][0],
              parsed_json['sfrplusResults']['V_conv_angle_degrees'][0]]

Rotation = parsed_json['sfrplusResults']['rotationDegrees']
SMIA_distortion = parsed_json['sfrplusResults']['SMIA_TV_Distortion_Pct']
# print len(SFR_Ny4)
# print len(Field_of_View)
# print 1
# # print len(max(Color_Aberration))
# print len(Tilt_Lens2Snsr)
# print len(Tilt_overall)
# print len(Rotation)
# print len(SMIA_distortion)
# print [max(Color_Aberration)]
output_before = IH+SFR_Ny4+Field_of_View+[max(Color_Aberration)]+Tilt_Lens2Snsr+Tilt_overall+Rotation+SMIA_distortion

# print output_after
# print output_before

plt.plot(IH[12:], SFR_Ny4[12:], 'rd', lw=3)
plt.grid(True)
plt.show()