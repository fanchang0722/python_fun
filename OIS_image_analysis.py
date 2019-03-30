import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pylab as plt

img = cv2.imread('frame000.jpg')
# ret, thresh1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
threshold = 100

BW = (img < threshold)

newImg = BW*(255-img)
center = ndimage.measurements.center_of_mass(newImg)
print(center)
# M = cv2.moments(newImg)
# print(M)
project_x = np.mean(newImg, 0)
project_y = np.mean(newImg, 1)

plt.figure(figsize=(16, 9))
plt.subplot(1, 3, 1)
plt.plot(project_x, '-r', lw=2)
plt.grid()
plt.subplot(1, 3, 2)
plt.plot(project_y, '-b', lw=2)
plt.grid()

# data(index,1)=x1;
# data(index,2)=y1;
# index = index+1;
# print img.shape
plt.subplot(1, 3, 3)
plt.imshow(255-img, cmap='gray')
# plt.hold()
plt.plot(center[0], center[1], 'ro')
plt.show()

# cv2.imshow('image', newImg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
