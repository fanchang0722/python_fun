#!/anaconda/bin/python
import matplotlib.pyplot as plt
from scipy.io import netcdf_file

ncf = netcdf_file(
    '/Users/fanchang/Downloads/Interactive Applications Using Matplotlib_Code/8846OS_01_Code/KTLX_20100510_22Z.nc')
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

cb.set_label('Reflectivity (dBZ)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()
