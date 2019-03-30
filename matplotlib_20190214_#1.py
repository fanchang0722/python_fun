import numpy as np
import matplotlib.pyplot as plt
# from pylab import show

x = np.arange(0, 2*np.pi, .1)
y = np.sin(x)
plt.plot(x, y)
plt.grid()
plt.show()