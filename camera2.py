import matplotlib.pyplot as plt
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
                 dimension=(2448, 3264), bayer='BGGR', sensor='IMX363'):
        self.filename = filename
        self.file_format = file_format
        self.dtype = dtype
        self.dimension = dimension
        self.bayer = bayer
        self.sensor = sensor
        # self.image = np.zeros(self.dimension)

    def __str__(self):
        return "%s  %r" % (self.__class__, self.__dict__)

    @property
    def raw_reader(self):
        if self.file_format == 'raw':
            temp = np.fromfile(self.filename, self.dtype)
            if self.sensor == 'IMX363':
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

    def LED_unifority(self, image, box):
        luma = 0.3 * image[:, :, 0] + 0.59 * image[:, :, 1] + 0.11 * image[:, :, 2]
        (cols, rows) = np.shape(luma)
        cols = cols/2
        rows = rows/2
        diagonalAngle = np.arctan(cols*1.0/rows)
        IH100 = np.floor(np.sqrt(cols**2 + rows**2))
        IH70 = np.floor(IH100*0.7)
        IH70OffsetRows = np.floor(IH70 * np.cos(diagonalAngle))
        IH70OffsetCols = np.floor(IH70 * np.sin(diagonalAngle))
        ROI = np.array([
            [rows-1, cols-1],
            [rows-IH70OffsetRows-1, cols-IH70OffsetCols-2],
            [rows+IH70OffsetRows-1, cols-IH70OffsetCols-2],
            [rows+IH70OffsetRows-1, cols+IH70OffsetCols],
            [rows-IH70OffsetRows-1, cols+IH70OffsetCols],
            [0, 0],
            [rows*2-1, 0],
            [rows*2-1, cols*2-1],
            [0, cols*2-1]
        ])
        box = np.array(box)
        Box = np.floor(box/2)
        RECT = np.ones([9, 6])
        RECT[0:5, 0] = ROI[0:5, 0]-Box[0]
        RECT[0:5, 1] = ROI[0:5, 1]-Box[1]
        RECT[0:5, 2] = box[0]
        RECT[0:5, 3] = box[1]
        RECT[5, 0:2] = ROI[5, :]
        RECT[5, 2] = box[0]
        RECT[5, 3] = box[1]
        RECT[6, 0] = ROI[6, 0]-box[0]
        RECT[6, 1] = ROI[6, 1]
        RECT[6, 2] = box[0]
        RECT[6, 3] = box[1]
        RECT[7, 0] = ROI[7, 0]-box[0]
        RECT[7, 1] = ROI[7, 1]-box[1]
        RECT[7, 2] = box[0]
        RECT[7, 3] = box[1]
        RECT[8, 0] = ROI[8, 0]
        RECT[8, 1] = ROI[8, 1]-box[1]
        RECT[8, 2] = box[0]
        RECT[8, 3] = box[1]
        RECT[:, 4] = RECT[:, 0]+box[0]
        RECT[:, 5] = RECT[:, 1] + box[1]
        statImage = np.ones([9, 7])
        for index in range(9):
            statImage[index, 0] = np.mean(np.mean(image[int(RECT[index, 1]):int(RECT[index, 5]), int(RECT[index, 0]):int(RECT[index, 4]), 2]))
            statImage[index, 1] = np.mean(np.mean(image[int(RECT[index, 1]):int(RECT[index, 5]), int(RECT[index, 0]):int(RECT[index, 4]), 1]))
            statImage[index, 2] = np.mean(np.mean(image[int(RECT[index, 1]):int(RECT[index, 5]), int(RECT[index, 0]):int(RECT[index, 4]), 0]))
            statImage[index, 3] = np.mean(
                np.mean(luma[int(RECT[index, 1]):int(RECT[index, 5]), int(RECT[index, 0]):int(RECT[index, 4])]))
        statImage[:, 4] = statImage[:, 0]/statImage[:, 1]
        statImage[:, 5] = statImage[:, 2] / statImage[:, 1]
        statImage[:, 6] = 100*statImage[:, 3] / statImage[0, 3]
        return statImage


if __name__ == '__main__':
    phoenix = Camera('/Users/fanchang/Downloads/20170403_4032x3032_YX_1_unpacked.raw', dimension=(3032, 4032), bayer='RGGB')
    # start = time.clock()
    image1 = phoenix.raw_reader
    output = phoenix.demosaic(image1)
    print(phoenix.LED_unifority(output, [100, 100]))
    Red = output[:, :, 0]
    Green = output[:, :, 1]
    Blue = output[:, :, 2]
    # print(np.max(np.max(image1)))
    # print (np.shape(output))



# plt.imshow(Red, cmap="binary")
# plt.show()
# print(np.shape(Red))
#     misc.imsave('/Users/fanchang/Downloads/test.png', output)
# print "1-->"+str(time.clock()-start)
# image2 = phoenix.awb(image1)
# misc.imsave('/Users/fanchang/Downloads/test3.png', image2)
# print "2-->"+str(time.clock()-start)
# start = time.clock()
# repeat = 1
# for index in range(repeat):
#     print "index-> "+str(index)
#     output = phoenix.demosaic(image1)
# print "Averaged time is-->"+str((time.clock()-start))
# print phoenix.__str__()

