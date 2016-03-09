# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:35:44 2016

@author: fanchang
"""
from PIL import Image

img = Image.open('/Users/fanchang/temp/60cm_8bit.png')
# img2=np.fromfile('/Users/fanchang/temp/60cm_0deg.tiff')
# plt.figure(figsize=(12,9))
# plt.imshow(img)
print img.size
print img.info
# print img2.shape
