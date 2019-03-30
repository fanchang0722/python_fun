import numpy as np
import matplotlib.pylab as plt
import cv2

width = 4000
height = 3000
filename = r'/Users/fanchang/Desktop/gray_patch_issue/EY3_6A31B000A9_40frame_chart.raw'
image = np.fromfile(filename, 'u2', width*height)
image = image.reshape(height, width)
plt.show(image[0:height:2, 0:width:2])
# new_img = np.zeros((width, height))
#
# # calculate mean of quad images
# mean_channel1 = np.mean(image[0:width:2, 0:height:2])
# mean_channel2 = np.mean(image[0:width:2, 1:height:2])
# mean_channel3 = np.mean(image[1:width:2, 0:height:2])
# mean_channel4 = np.mean(image[1:width:2, 1:height:2])
# # calculate gain for quad images
# max_gain = np.max([mean_channel1, mean_channel2,
#                    mean_channel3, mean_channel4])
# channel_gain = max_gain / np.array([mean_channel1, mean_channel2,
#                                     mean_channel3, mean_channel4])
# # print channel_gain
# # apply gain on quad images
# new_img[0:width:2, 0:height:2] = np.uint16(image[0:width:2, 0:height:2] * channel_gain[0])
# new_img[0:width:2, 1:height:2] = np.uint16(image[0:width:2, 1:height:2] * channel_gain[1])
# new_img[1:width:2, 0:height:2] = np.uint16(image[1:width:2, 0:height:2] * channel_gain[2])
# new_img[1:width:2, 1:height:2] = np.uint16(image[1:width:2, 1:height:2] * channel_gain[3])
cv2.imwrite('/Users/fanchang/Desktop/test.png', image)
# rgb = cv2.cvtColor(new_img, cv2.COLOR_BAYER_BG2RGB)
# cv2.imwrite('/Users/fanchang/Desktop/rgb.png', rgb)