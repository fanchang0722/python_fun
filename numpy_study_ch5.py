import matplotlib.pyplot as plt
import numpy as np


def ultimate_answer(a):
    result = np.zeros_like(a)
    result.flat = 42
    return result


ufunc = np.frompyfunc(ultimate_answer, 1, 1)
print ufunc(np.arange(6).reshape(2, 3))

a = 9
b = 8
t = np.linspace(-np.pi, np.pi, 1001)
x = np.sin(a * t + np.pi / 2)
y = np.sin(b * t)
plt.plot(x, y)
plt.grid()
plt.show()
