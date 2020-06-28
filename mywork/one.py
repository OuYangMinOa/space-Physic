import pandas as pd
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import time
class path:
    def __init__(self):
        self.floder = r"D:\space physic\FORMOSAT1\2000"
        self.m = Basemap()
        self.m.drawcoastlines()
        self.m.fillcontinents()
        self.m.drawparallels(np.arange(-90,90,30),labels=[1,1,0,1], fontsize=8)
        self.m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1], rotation=45, fontsize=8)
        plt.xlabel('Longitude', labelpad=40)
        plt.ylabel('Latitude', labelpad=40)
        self.get_all_file()
        self.plot_show()
    def get_all_file(self):
        self.all_file = [i for i in os.listdir(self.floder)]
        #self.all_file.extend([i for i in os.listdir(r"D:\space physic\FORMOSAT1\2001")])
    def read_file(self,file):
        df = pd.read_table(self.floder+"\\"+file,sep="\s+|:",engine='python')
        return df["GLAT"][:].values, df["GLON"][:].values,df["HH"][:].values,df["MM"][:].values,df["SS"][:].values
    def plot_show(self):
        
        for file in self.all_file[:1]:
            print(file)
            latitude, longitude,hh,mm,ss = self.read_file(file)
            for i in range(5):
                plt.pause(0.2)
            for i in range(0,86000,60):
                    plt.title(f"{hh[i]}:{mm[i]}:{ss[i]}")
                    x,y = self.m(180-longitude[i],latitude[i])
                    self.m.scatter(x,y,10,c='m',zorder=3)
                    plt.pause(0.0001)
        plt.show()
path()
