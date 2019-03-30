import os
import sys
import numpy as np
from scipy.signal import convolve2d as conv2
import matplotlib.pylab as plt
from PIL import Image
import cv2


def centroid(x):
    addsum = 0
#    print len(x)
    for coordinate in range(len(x)):
#        print coordinate, x[coordinate]
        addsum += coordinate*x[coordinate]
#    print addsum
    return addsum/len(x)


def ahamming(n, mid):
    wid1 = mid-1
    wid2 = n-mid
    wid = np.max([wid1, wid2])
    windows=[]
    for ix in range(n):
        arg = ix-mid
        windows.append(0.54+0.46*np.cos(np.pi*arg/wid))
    return windows


fileName = r'/Users/fanchang/python_fun/test.png'
img = Image.open(fileName, mode="r")
# img.show()

imgArray = np.array(img)
[rows, cols] = np.shape(imgArray)
# print rows, cols
kernal = np.array([-0.5, 0, 0.5])
len_kernal = len(kernal)
temp = np.convolve(imgArray[0, :], kernal, 'full')

Edge = temp[len_kernal:cols]
head = []
for index in range(len_kernal):
    head.append(temp[len_kernal])
Edge = np.concatenate((np.array(head), Edge))
print cols-centroid(Edge*ahamming(cols,np.floor((cols+1)/2)))
#print Edge
plt.figure(figsize=(12,9))
plt.plot(Edge)
plt.plot(Edge*ahamming(cols,np.floor((cols+1)/2)))
plt.show()
