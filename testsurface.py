import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from netCDF4 import Dataset
import os

m = Basemap()
m.drawcoastlines()
m.fillcontinents()
m.drawparallels(np.arange(-90,90,30),labels=[1,1,0,1], fontsize=8)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,0,1], rotation=45, fontsize=8)
plt.xlabel('Longitude', labelpad=40)
plt.ylabel('Latitude', labelpad=40)

x = np.arange(-90,90,1)
y = np.arange(-180,180,1)
x,y = np.meshgrid(x,y)
z = np.sin(x/100)**10 + np.cos(10 + y*x/10000) * np.cos(x/100)

##mappable = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
##mappable.set_array(z)
print(z.shape)

m.pcolormesh(y,x,z,zorder=2,cmap='Spectral_r',alpha=0.7)
plt.colorbar()
plt.show()
