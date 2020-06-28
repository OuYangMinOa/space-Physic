import pandas as pd
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import time
class ion:
    def __init__(self):
        self.floder_2000 = r"D:\space physic\FORMOSAT1\2000"
        self.floder_2001 = r"D:\space physic\FORMOSAT1\2001"
        dx = 15
        dy = 15
        self.x = np.arange(-180,180+dx,dx)
        self.y = np.arange(-90,90+dy,dy)
        self.sa =   np.zeros((len(self.x),len(self.y),1)).tolist()
        self.z = np.zeros((len(self.x),len(self.y)))#.tolist()
        self.this_max = 100
        x_index = np.where(self.x <= 178 )[0][-1]
        y_index = np.where(self.y <= -12 )[0][-1]
        #self.get_year_day(2000,1,3) 
    def map__init(self):
        self.m = Basemap()
        self.m.drawcoastlines()
        self.m.fillcontinents()
        self.m.drawparallels(np.arange(-90,90,30),labels=[1,1,0,1], fontsize=8)
        self.m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1], rotation=45, fontsize=8)
        plt.xlabel('Longitude', labelpad=40)
        plt.ylabel('Latitude', labelpad=40)

    def ion_year_day(self,y,arange):
        plt.title("N")
        if y==2000:
            self.all_file = [self.floder_2000 + "\\"+i for i in os.listdir(self.floder_2000)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                self.add_in_Lattice(now["GLAT"][:].values,now["GLON"][:].values,now["LogN"][:].values)
        if y==2001:
            self.all_file = [self.floder_2001 + "\\"+i for i in os.listdir(self.floder_2001)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                self.add_in_Lattice(now["GLAT"][:].values,now["GLON"][:].values,now["LogN"][:].values)
    def O2(self,y,arange):
        plt.title("o+")
        if y==2000:
            self.all_file = [self.floder_2000 + "\\"+i for i in os.listdir(self.floder_2000)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                self.add_in_Lattice(now["GLAT"][:].values,now["GLON"][:].values,now["O+"][:].values)
        if y==2001:
            self.all_file = [self.floder_2001 + "\\"+i for i in os.listdir(self.floder_2001)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                self.add_in_Lattice(now["GLAT"][:].values,now["GLON"][:].values,now["O+"][:].values)
    def O2_day(self,y,arange):
        plt.title("o+ day")
        if y==2000:
             self.all_file = [self.floder_2000 + "\\"+i for i in os.listdir(self.floder_2000)]
             for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [11,12,13])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["O+"][:].values[codition])
        if y==2001:
            self.all_file = [self.floder_2001 + "\\"+i for i in os.listdir(self.floder_2001)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [11,12,13])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["O+"][:].values[codition])
    def O2_nigth(self,y,arange):
        plt.title("o+ night")
        if y==2000:
             self.all_file = [self.floder_2000 + "\\"+i for i in os.listdir(self.floder_2000)]
             for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [0,23,1])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["O+"][:].values[codition])
        if y==2001:
            self.all_file = [self.floder_2001 + "\\"+i for i in os.listdir(self.floder_2001)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [0,23,1])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["O+"][:].values[codition])

                
    def day(self,y,arange):
        if y==2000:
             self.all_file = [self.floder_2000 + "\\"+i for i in os.listdir(self.floder_2000)]
             for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [11,12,13])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["LogN"][:].values[codition])
        if y==2001:
            self.all_file = [self.floder_2001 + "\\"+i for i in os.listdir(self.floder_2001)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [11,12,13])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["LogN"][:].values[codition])
                
    def nigth(self,y,arange):
        if y==2000:
             self.all_file = [self.floder_2000 + "\\"+i for i in os.listdir(self.floder_2000)]
             for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [0,23,1])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["LogN"][:].values[codition])
        if y==2001:
            self.all_file = [self.floder_2001 + "\\"+i for i in os.listdir(self.floder_2001)]
            for i in arange:
                now =  pd.read_table(self.all_file[i],sep="\s+|:",engine='python')
                codition = [i for i,va in enumerate(now["LH"][:].values) if (int(va) in [0,23,1])]
                self.add_in_Lattice(now["GLAT"][:].values[codition],now["GLON"][:].values[codition],now["LogN"][:].values[codition])
                
    def add_in_Lattice(self,lat,lon,logn):
        for at,on,n in zip(lat,lon,logn):
            try:
                x_index = np.where(self.x <= 180-on )[0][-1]
                y_index = np.where(self.y <= at  )[0][-1]
            except Exception as e:
                print(on,at,e)
            if (self.sa[x_index][y_index]==[0]):
                self.sa[x_index][y_index] = [n]
            else:
                self.sa[x_index][y_index].append(n)
            if (n < self.this_max):
                self.this_max = n
    def process_plot(self):
        for x_index in range(len(self.x)):
            for y_index in range(len(self.y)):
                self.z[x_index,y_index] = np.median(self.sa[x_index][y_index])
        self.map__init()
        
        X,Y = np.meshgrid(self.x,self.y)
        print(Y.shape,X.shape,self.z.shape)
##        np.partition(self.z, )[n]#=
        self.m.contourf(X,Y,self.z.T,zorder=2,cmap='rainbow',vmax = np.max(self.z),vmin =np.min(self.z))
        print(f"min = {self.this_max}")
        self.m.drawcoastlines()
        plt.colorbar()
        plt.show()

if __name__=="__main__":
    spring  = [i for i in range(36,127)]
    summer  = [i for i in range(128,219)]
    autumn = [i for i in range(220,311)]
    winter = [i for i in range(311,366)] + [i for i in range(1,44)]
    #print(winter)
    ii = ion()
##    ii.ion_year_day(2000,winter)
##    ii.process_plot()
    ii.ion_year_day(2001,summer)#[ i for i in range(0,10)])
    ii.process_plot()










    
