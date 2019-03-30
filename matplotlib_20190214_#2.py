from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Tkinter as tk
import matplotlib.pylab as plt

fig = Figure(figsize=(12, 8), facecolor='white')

axis = fig.add_subplot(211)

xvalues = [1, 2, 3, 4]
yvalues = [5, 7, 6, 8]

axis.plot(xvalues, yvalues)

axis.set_xlabel('Horizontal label')
axis.set_ylabel('Vertical label')

axis.grid(linestyle='-')
plt.subplot(2, 1, 1)
plt.plot(xvalues, yvalues)
plt.xlabel('Horizontal label')
plt.ylabel('Vertical label')
plt.legend("test")
plt.show()
def _destroyWindow():
	root.quit()
	root.destroy()