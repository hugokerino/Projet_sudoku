# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:24:30 2023

@author: hugob
"""

import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray
from skimage.transform import resize, rotate

from functions import plot_num, plot_4num, test_correlate_num
     
x_resize = 30
y_resize = 30


#Import data reference
data = Path().cwd() / 'data' / 'data_train' / 'num'

k = 1
tab_num0 = []
tab_num90 = []
tab_num180 = []
tab_num270 = []

for f in data.rglob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize((img - np.mean(img))/np.std(img),(x_resize,y_resize),anti_aliasing=True) #Standardization
    tab_num0.append((img,k)) # Reference images
    tab_num90.append((rotate(img,90),k))
    tab_num180.append((rotate(img,180),k))
    tab_num270.append((rotate(img,270),k))
    k += 1
   
    
#Import data test
data_test = Path().cwd() / 'data' / 'data_test' 

num_sudoku1 = data_test / 'Sudoku3' / 'num'
tab_num_sudoku1 = []
for f in num_sudoku1.glob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f)))
    img = resize(img,(x_resize,y_resize),anti_aliasing=True)
    tab_num_sudoku1.append((img,int(f.name[0])))


num_sudoku2 = data_test / 'Sudoku4' / 'num'    
tab_num_sudoku2 = []
for f in num_sudoku2.glob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f)))
    img = resize(img,(x_resize,y_resize),anti_aliasing=True)
    tab_num_sudoku2.append((img,int(f.name[0])))
    
    
#Rotate numbers
tab_num_sudoku5 = []
tab_num_sudoku6 = []
tab_num_sudoku7 = []
for k in range(len(tab_num_sudoku1)):
    tab_num_sudoku5.append((rotate(tab_num_sudoku1[k][0],90),tab_num_sudoku1[k][1]))
    tab_num_sudoku6.append((rotate(tab_num_sudoku1[k][0],180),tab_num_sudoku1[k][1]))
    tab_num_sudoku7.append((rotate(tab_num_sudoku1[k][0],270),tab_num_sudoku1[k][1]))

def plot_num_ref(imgs,i):
    plt.figure(i)
    nbr_num = len(imgs)
    for i in range(nbr_num):
        plt.subplot(5,5,i+1)
        plt.imshow(imgs[i][0],cmap='binary')
        plt.title(str(i))
        
plot_num_ref(tab_num0, 1)
plot_num_ref(tab_num90, 2)
plot_num_ref(tab_num180, 3)
plot_num_ref(tab_num270, 4)

# Algo 

# First part : detect the correct rotation beetween 0,90,180,270

n = 4
img_test = tab_num_sudoku1[n][0]
print(f"Number to detect = {tab_num_sudoku1[n][1]}")

list_etallon = (3,4,5)
autocor_thres = []
for num in list_etallon:
    autocor_thres.append(np.sum(tab_num0[num][0]*tab_num0[num][0])*0.9)
    autocor_0 = scipy.signal.correlate(tab_num0[num-1][0],img_test,mode = 'same',method='fft')  
    
    

    
    