# //anaconda/bin/python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

temp = np.fromfile('/Users/fanchang/temp/60cm.raw', dtype='int16')
width = 3264
height = 2448
img = np.reshape(temp, (height, width))

print np.max(np.max(img))
# (height,width) = img.shape
# print width
img2 = Image.open('/Users/fanchang/temp/60cm_8bit.png')
plt.figure(figsize=(12, 9))
plt.subplot(121)
plt.imshow(img[0:height:2, 0:width:2], cmap='binary_r')

plt.subplot(122)
plt.imshow(np.array(img2))
plt.show()
# (width2,height2) = img2.size
# print width2
# z = np.zeros((8, 8), dtype='float')
# z[0:8:2, 0:8:2] = 1
# kernel = np.array([[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]])
# z2 = conv2(z, kernel, boundary='wrap', mode='same')
# print z
# print z2
