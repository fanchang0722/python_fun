import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pylab as plt


def OIS_calculation(fileName, imgThreshold, imgRange):
    data = np.zeros((100, 2))
    cap = cv2.VideoCapture(fileName)
    ret = True
    count = 0
    while ret:
        ret, img = cap.read()
        if img is not None:
            # print img.shape
            newImg = img[imgRange[0]:imgRange[1], imgRange[2]:imgRange[3]]
            newImg = 0.299 * newImg[:, :, 0] + 0.587 * newImg[:, :, 1] + 0.114 * newImg[:, :, 2]
            BW = (newImg < imgThreshold)
            newImg = BW * (255 - newImg)
            center = ndimage.measurements.center_of_mass(newImg)
            data[count, :] = center
            cv2.imwrite(g % count, newImg)
            count += 1
    print(count)
    print("%.3f" % (np.max(data[count-20:count-1, 0])-np.min(data[count-20:count-1, 0])))
    print("%.3f" % (np.max(data[count-20:count-1, 1])-np.min(data[count-20:count-1, 1])))
    plt.plot(data[count-20:count-1, 0], 'r>', markersize=10)
    plt.plot(data[count-20:count-1, 1], 'g<', markersize=10)
    plt.grid()
    plt.show()


imgThreshold = 100
imgRange = [250, 500, 500, 690]
fileName = r'C:\Users\fanchang\Downloads\mode2.mp4'
print OIS_calculation(fileName, imgThreshold, imgRange)