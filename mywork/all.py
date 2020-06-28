import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from netCDF4 import Dataset
import os
import time

class for3:
    def __init__(self):
        self.nn = time.time()
        self.f_allday()
        self.show_keys()
        self.colormap=['b','g','r','c','m','y']

        dx = 5
        dy = 5
        self.x = np.arange(-180,180+dx,dx)
        self.y = np.arange(-90,90+dy,dy)
        self.sa =   np.zeros((len(self.x),len(self.y),1)).tolist()
        
        self.z = np.zeros((len(self.x),len(self.y)))
        

        
    def f_allday(self,arange=[i for i in range(1,366)]):
        self.all_file = []
        self.all_time = []
        self.satellite = []
        for i in arange:
            floder = f"D:\\space physic\\FORMOSAT3\\2007\\2007.{i:>03d}"
            for file in os.listdir(floder):
                self.all_file.append(floder+"\\"+file)
                self.all_time.append(file.split('.')[3:5])
                self.satellite.append(int(file.split('.')[0][-1]))
    def path_1_6(self):
        self.map_init()
        for i,file in enumerate(self.all_file):
            sa = self.satellite[i]
            if (sa!=6):
                continue
            nc = Dataset(file)
            #condition = [num for num,i in enumerate(nc.variables['MSL_alt'][:].compressed()) if (i>295 and i<305)]
            latitude =  nc.variables['GEO_lat'][:].compressed()#[condition]
            longitude = nc.variables['GEO_lon'][:].compressed()#[condition]
            self.m.scatter(longitude,latitude,color=self.colormap[sa-1] ,label=sa if (self.satellite[i-1]!=sa) else None,zorder=3)
        plt.title("2007 day1 one day satellite 6")
        plt.legend()
        plt.show()
    def show_keys(self):
        if (self.all_file != []):
            nc = Dataset(self.all_file[0])
            print(nc.variables.keys())
    def alt_ele(self,file):
        nc = Dataset(  self.all_file[file])
        time_ = self.all_time[file]
        
        MSL_alt =  nc.variables['MSL_alt'][:].compressed()
        ELEC_dens = nc.variables['ELEC_dens'][:].compressed()
        plt.title(f"2007 {time_[0]}:{time_[1]} day 1")
        plt.plot(ELEC_dens,MSL_alt)
        plt.show()

    def full_ele(self,arange):
        self.f_allday(arange)
        for file in self.all_file:
            nc = Dataset(file)
            condition = [num for num,i in enumerate(nc.variables['MSL_alt'][:].compressed()) if (i>295 and i<305)]
            ELEC_dens = nc.variables['ELEC_dens'][:].compressed()[condition]
            latitude =  nc.variables['GEO_lat'][:].compressed()[condition]
            longitude = nc.variables['GEO_lon'][:].compressed()[condition]
            self.add_in_Lattice(latitude,longitude,ELEC_dens)
            
    def add_in_Lattice(self,lat,lon,logn):
        for at,on,n in zip(lat,lon,logn):
            try:
                x_index = np.where(self.x <= on )[0][-1]
                y_index = np.where(self.y <= at  )[0][-1]
            except Exception as e:
                print(on,at,e)
            if (self.sa[x_index][y_index]==[0]):
                self.sa[x_index][y_index] = [n]
            else:
                self.sa[x_index][y_index].append(n)
                
    def process_plot(self):
        for x_index in range(len(self.x)):
            for y_index in range(len(self.y)):
                self.z[x_index,y_index] = np.median(self.sa[x_index][y_index])
        self.map_init()
        
        X,Y = np.meshgrid(self.x,self.y)
        print(Y.shape,X.shape,self.z.shape)
        print(abs(time.time()-self.nn))
        self.m.contourf(X,Y,self.z.T,zorder=2,cmap='rainbow',vmax = np.max(self.z),vmin=np.min(self.z))
        self.m.drawcoastlines()
        plt.colorbar()
        plt.show()
        
    def map_init(self):
        self.m = Basemap()
        self.m.drawcoastlines()
        self.m.fillcontinents()
        self.m.drawparallels(np.arange(-90,90,30),labels=[1,1,0,1], fontsize=8)
        self.m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1], rotation=45, fontsize=8)
        plt.xlabel('Longitude', labelpad=40)
        plt.ylabel('Latitude', labelpad=40)




if __name__ =="__main__":
    spring  = [i for i in range(36,127)]
    summer  = [i for i in range(128,219)]
    autumn = [i for i in range(220,311)]
    winter = [i for i in range(311,366)] + [i for i in range(1,44)]
    ii = for3()
    ii.full_ele(winter)
    ii.process_plot()
    












