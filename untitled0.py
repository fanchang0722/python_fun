# import matplotlib.pyplot as plt
import scipy.signal as sd
from scipy import misc
import numpy as np
from PIL import Image
import time


class Camera(object):
    """
    Camera class
    """

    def __init__(self, filename, file_format='raw', dtype='<u2',
                 dimension=(2448, 3264), bayer='BGGR'):
        self.filename = filename
        self.file_format = file_format
        self.dtype = dtype
        self.dimension = dimension
        self.bayer = bayer
        # self.image = np.zeros(self.dimension)

    def __str__(self):
        return "%s  %r" % (self.__class__, self.__dict__)

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
        :type image: object
        :param : bayer image
        """
        # create same dimension image
        (width, height) = self.dimension
        new_img = np.zeros(self.dimension)

        # calculate mean of quad images
        mean_channel1 = np.mean(image[0:width:2, 0:height:2])
        mean_channel2 = np.mean(image[0:width:2, 1:height:2])
        mean_channel3 = np.mean(image[1:width:2, 0:height:2])
        mean_channel4 = np.mean(image[1:width:2, 1:height:2])
        # calculate gain for quad images
        max_gain = np.max([mean_channel1, mean_channel2,
                           mean_channel3, mean_channel4])
        channel_gain = max_gain / np.array([mean_channel1, mean_channel2,
                                            mean_channel3, mean_channel4])
        # print channel_gain
        # apply gain on quad images
        new_img[0:width:2, 0:height:2] = np.uint16(image[0:width:2, 0:height:2] * channel_gain[0])
        new_img[0:width:2, 1:height:2] = np.uint16(image[0:width:2, 1:height:2] * channel_gain[1])
        new_img[1:width:2, 0:height:2] = np.uint16(image[1:width:2, 0:height:2] * channel_gain[2])
        new_img[1:width:2, 1:height:2] = np.uint16(image[1:width:2, 1:height:2] * channel_gain[3])
        return new_img

    def demosaic(self, image):
        (width, height) = self.dimension
        # quad 1
        mask = np.zeros(self.dimension)
        mask[0:width:2, 0:height:2] = 1
        quad1 = image*mask
        # quad 2
        mask = np.zeros(self.dimension)
        mask[0:width:2, 1:height:2] = 1
        quad2 = image*mask
        # quad 3
        mask = np.zeros(self.dimension)
        mask[1:width:2, 0:height:2] = 1
        quad3 = image*mask
        # quad 4
        mask = np.zeros(self.dimension)
        mask[1:width:2, 1:height:2] = 1
        quad4 = image*mask
        # convolution kernel
        non_green_kernel = np.array([[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]])
        green_kernel = np.array([[0, 0.25, 0], [0.25, 1.0, 0.25], [0, 0.25, 0]])
        output = np.zeros((width, height, 3))
        if self.bayer == 'RGGB':
            red = quad1
            red = sd.convolve2d(red, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            green = quad2+quad3
            green = sd.convolve2d(green, green_kernel, boundary='wrap', mode='same')*255/1023.
            blue = quad4
            blue = sd.convolve2d(blue, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            output[:, :, 0] = np.uint8(red)
            output[:, :, 1] = np.uint8(green)
            output[:, :, 2] = np.uint8(blue)
            # return output

        if self.bayer == 'BGGR':
            red = quad4
            red = sd.convolve2d(red, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            green = quad2+quad3
            green = sd.convolve2d(green, green_kernel, boundary='wrap', mode='same')*255/1023.
            blue = quad1
            blue = sd.convolve2d(blue, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            output[:, :, 0] = np.uint8(red)
            output[:, :, 1] = np.uint8(green)
            output[:, :, 2] = np.uint8(blue)
            # return output

        if self.bayer == 'GBRG':
            red = quad3
            red = sd.convolve2d(red, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            green = (quad1+quad4)
            green = sd.convolve2d(green, green_kernel, boundary='wrap', mode='same')*255/1023.
            blue = quad2
            blue = sd.convolve2d(blue, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            output[:, :, 0] = np.uint8(red)
            output[:, :, 1] = np.uint8(green)
            output[:, :, 2] = np.uint8(blue)
            # return output

        if self.bayer == 'GRBG':
            red = quad2
            red = sd.convolve2d(red, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            green = (quad1+quad4)
            green = sd.convolve2d(green, green_kernel, boundary='wrap', mode='same')*255/1023.
            blue = quad3
            blue = sd.convolve2d(blue, non_green_kernel, boundary='wrap', mode='same')*255/1023.
            output[:, :, 0] = np.uint8(red)
            output[:, :, 1] = np.uint8(green)
            output[:, :, 2] = np.uint8(blue)
        return output

phoenix = Camera('/Users/fanchang/Desktop/sfrplus.raw', bayer='BGGR')
start = time.clock()
image1 = phoenix.raw_reader
output = phoenix.demosaic(image1)
misc.imsave('/Users/fanchang/Desktop/test2.png', output)
# print "1-->"+str(time.clock()-start)
image2 = phoenix.awb(image1)
# print "2-->"+str(time.clock()-start)
start = time.clock()
repeat = 10
for index in range(repeat):
    print "index-> "+str(index)
    output = phoenix.demosaic(image1)
print "Averaged time is-->"+str((time.clock()-start)/repeat/1.0)
# print phoenix.__str__()

