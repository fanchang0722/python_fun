# //anaconda/bin/python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# def AWB(raw_img):
#     """
#     Perform global auto white balance (AWB)
#     """
#
#     # create same dimension image
#     (width, height) = img.shape
#     new_img = np.zeros((width, height))
#     # separate quad bayer image
#     channel1 = img[0:width:2, 0:height:2]
#     channel2 = img[0:width:2, 1:height:2]
#     channel3 = img[1:width:2, 0:height:2]
#     channel4 = img[1:width:2, 1:height:2]
#     # calculate mean of quad images
#     mean_channel1 = np.mean(channel1)
#     mean_channel2 = np.mean(channel2)
#     mean_channel3 = np.mean(channel3)
#     mean_channel4 = np.mean(channel4)
#     # calculate gain for quad images
#     max_gain = np.max([mean_channel1, mean_channel2, mean_channel3, mean_channel4])
#     channel_gain = max_gain / np.array([mean_channel1, mean_channel2, mean_channel3, mean_channel4])
#     # apply gain on quad images
#     new_img[0:width:2, 0:height:2] = channel1 * channel_gain[0]
#     new_img[0:width:2, 1:height:2] = channel2 * channel_gain[1]
#     new_img[.1:width:2, 0:height:2] = channel3 * channel_gain[2]
#     new_img[1:width:2, 1:height:2] = channel4 * channel_gain[3]
#     return new_img
#
#
# def Demosaic(raw_img, bayer_pattern):
#     """
#     Perform bilinear demosaic calculation
#     """
#     kernel=np.array([[1/4, 1/2, 1/4], [1/2, 1, 1/2], [1/4, 1/2, 1/4]])
#     conv2(raw_img, kernel, boundary='wrap', mode='same')


class Camera(object):
    """
    Camera class
    """

    def __init__(self, filename, file_format='raw', dtype='<u2',
                 dimension=(2448, 3264), bayer='RGGB'):
        self.filename = filename
        self.file_format = file_format
        self.dtype = dtype
        self.dimension = dimension
        self.bayer = bayer
        # self.image = np.zeros(self.dimension)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    @property
    def raw_reader(self):
        if self.file_format == 'raw':
            temp = np.fromfile(self.filename, self.dtype)
            return np.reshape(temp, self.dimension)
        else:
            return Image.open(self.filename)

    def awb(self, image):
        """
        Perform global auto white balance (AWB)
        :param image: bayer image
        """
        # create same dimension image
        (width, height) = self.dimension
        new_img = np.zeros(self.dimension)

        # separate quad bayer image
        channel1 = image[0:width:2, 0:height:2]
        channel2 = image[0:width:2, 1:height:2]
        channel3 = image[1:width:2, 0:height:2]
        channel4 = image[1:width:2, 1:height:2]
        # calculate mean of quad images
        mean_channel1 = np.mean(channel1)
        mean_channel2 = np.mean(channel2)
        mean_channel3 = np.mean(channel3)
        mean_channel4 = np.mean(channel4)
        # calculate gain for quad images
        max_gain = np.max([mean_channel1, mean_channel2,
                           mean_channel3, mean_channel4])
        channel_gain = max_gain / np.array([mean_channel1, mean_channel2,
                                            mean_channel3, mean_channel4])
        # apply gain on quad images
        new_img[0:width:2, 0:height:2] = channel1 * channel_gain[0]
        new_img[0:width:2, 1:height:2] = channel2 * channel_gain[1]
        new_img[1:width:2, 0:height:2] = channel3 * channel_gain[2]
        new_img[1:width:2, 1:height:2] = channel4 * channel_gain[3]
        return new_img

    def demosaic(self, image):
        kernel = np.array([[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]])
        pass


phoenix = Camera('/Users/fanchang/temp/60cm.raw')
# print phoenix.raw_reader.__dict__
image1 = phoenix.raw_reader
image2 = phoenix.awb(image1)
print phoenix.__str__()

# temp = np.fromfile('/Users/fanchang/temp/60cm.raw', dtype='<u2')
# img = np.reshape(temp, (2448, 3264))
# Img = AWB(img)
#
plt.figure(figsize=(12, 9))
plt.subplot(121)
plt.imshow(image1, cmap='gist_gray')

plt.subplot(122)
plt.imshow(image2, cmap='gist_gray')
plt.show()
# # (width2,height2) = img2.size
# # print width2
# # z = np.zeros((8, 8), dtype='float')
# # z[0:8:2, 0:8:2] = 1
# # kernel = np.array([[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]])
# # z2 = conv2(z, kernel, boundary='wrap', mode='same')
# # print z
# # print z2
#
# img2 = Image.open('/Users/fanchang/temp/60cm_8bit.png')
