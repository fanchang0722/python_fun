import numpy as np
x = np.random.uniform(0, 1, 10000)
xbar = np.mean(x)
xstd = np.std(x)
print '{0:.4f}'.format(xbar)
print '{0:.4f}'.format(xstd)