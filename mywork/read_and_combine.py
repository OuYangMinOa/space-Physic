import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(multiple=True) # show an "Open" dialog box and return the path to the selected file
print(len(filename))
get = eval(input("columns :"))
rows = int(len(filename)/get)
image = cv2.imread(filename[0])[73:434-73,126:846]
now_image = 1
print(f"{get} x {rows}")
for i in range(rows-1):
    if (now_image==len(filename)):
        break
    image_2 = cv2.imread(filename[now_image])[73:434-73,126:846]
    image = np.vstack((image, image_2))
    now_image += 1
print(now_image)
if (now_image<len(filename)):
    for j in range(get-1):
        image_v = cv2.imread(filename[now_image])[73:434-73,126:846]
        now_image += 1
        for i in range(rows-1):
            image_2 = cv2.imread(filename[now_image])[73:434-73,126:846]
            image_v = np.vstack((image_v, image_2))
            now_image += 1
        image = np.hstack((image, image_v))
    

name = "\\".join(filename[0].split('\\')[:-2])+"combine.png"
cv2.imwrite(name,image)
print("==== end ====")
