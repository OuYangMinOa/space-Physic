import pandas as pd
import os
floder_2000 = r"D:\space physic\FORMOSAT1\2000"
floder_2001 = r"D:\space physic\FORMOSAT1\2001"

floder_2000_csv = r"D:\space physic\FORMOSAT1\2000_csv"
floder_2001_csv = r"D:\space physic\FORMOSAT1\2001_csv"



all_file_2000 = [floder_2000 + "\\"+i for i in os.listdir(floder_2000)]
all_file_2001 = [floder_2001 + "\\"+i for i in os.listdir(floder_2001)]



def to_ccc(floder,to_file):
    for num,i in enumerate(floder):
        now =  pd.read_table(i,sep="\s+|:",engine='python')
        d = {'time':now["LH"][:].values,
             'GEO_lon':180-now["GLON"][:].values,
             'ELEC_dens':now["LogN"][:].values,
             'GEO_lat':now["GLAT"][:].values,
             'MSL_alt':now["ALT"][:].values}
        df = pd.DataFrame(data=d)
        fieee = f'{num}'.zfill(3)
        print(f"{to_file}\\{fieee}.csv")
        df.to_csv(f"{to_file}\\{fieee}.csv", encoding='utf-8', index=False)
        
to_ccc(all_file_2000,floder_2000_csv)
to_ccc(all_file_2001,floder_2001_csv)
