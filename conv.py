import numpy as np
import scipy.signal as sd

def convolution2d(inputX, kernel):
    m, n = kernel.shape
    if m == n:
        y, x = inputX.shape
        y = y + 2*m - 2
        x = x + 2*m - 2
        outputY = np.zeros((y, x))
        paddinginputX = outputY
        paddinginputX[m - 1:y + 1 - m, m - 1:x + 1 - m] = inputX
        for i in range(y-m+1):
            for j in range(x-m+1):
                outputY[i][j] = np.sum(paddinginputX[i:i + m, j:j + m] * np.flipud(np.fliplr(kernel)))
                print outputY[i][j]
    return outputY[:y + 1 - m, :x + 1 - m]



image = np.transpose(np.arange(1, 10, 1).reshape((3, 3)))
print image
# kernal = np.ones([5, 5])

kernal = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
print(kernal)
convResult = convolution2d(image, kernal)
print(convResult)
print("\n")
new1 = sd.convolve2d(image, kernal)
print(new1)