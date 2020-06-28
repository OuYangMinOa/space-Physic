import os

floder_2000_csv = r"D:\space physic\FORMOSAT1\2000_csv"

all_file_2000_csv = [floder_2000_csv + "\\"+i for i in os.listdir(floder_2000_csv)]

for i in all_file_2000_csv:
    sp = i.split("\\")
    dire,dile = '\\'.join(sp[0:-1]),sp[-1].zfill(7)
    os.rename(i,dire+"\\"+dile)
