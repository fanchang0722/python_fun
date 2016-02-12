#!/anaconda/bin/python

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.io import netcdf_file

from tutorial import polygon_loader

ncf = netcdf_file('KTLX_20100510_22Z.nc')
data = ncf.variables['Reflectivity']
lats = ncf.variables['lat']
lons = ncf.variables['lon']
i = 0

cmap = plt.get_cmap('gist_ncar')
cmap.set_under('lightgrey')

fig, ax = plt.subplots(1, 1)
im = ax.imshow(data[i], origin='lower',
               extent=(lons[0], lons[-1], lats[0], lats[-1]),
               vmin=0.1, vmax=80, cmap='gist_ncar')
cb = fig.colorbar(im)

polygons = polygon_loader('polygons.shp')
for poly in polygons[i]:
    p = Polygon(poly, lw=3, fc='k', ec='w', alpha=0.45)
    ax.add_artist(p)
cb.set_label("Reflectivity (dBZ)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.show()
