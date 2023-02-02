# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 13:23:14 2023

@author: hugob

Test with real data of functions created in reco_num.py 

"""

import numpy as np
import scipy.ndimage
import scipy.signal
from matplotlib import pyplot as plt
from pathlib import Path

from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray
from skimage import filters
from skimage.transform import resize, rotate
from skimage.morphology import erosion, dilation 

from reco_num import plot_num, plot_4num, shift_img, correlate_img,correlate_img_FFT, stat_img
from reco_num import gradient_morphology,test_correlate,test_correlate_num, seuillage

#Import data
data = Path().cwd() / 'data' / 'num_police1'

tab_num = []
for f in data.rglob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize(img,(25,40),anti_aliasing=True)
    #img = resize((img - np.mean(img))/np.std(img),(25,40),anti_aliasing=True) #Standardization
    tab_num.append(img) # Reference images


#Load data test
data_test = Path().cwd() / 'data' / 'data_test'

num_sudoku1 = data_test / 'Sudoku1' / 'num'
tab_num_sudoku1 = []
for f in num_sudoku1.glob("*.jpg"):
    img = rotate(rgb2gray(img_as_float(io.imread(f))),angle = 90,resize = True)
    img = resize(img,(25,40),anti_aliasing=True)
    #img = resize((img - np.mean(img))/np.std(img),(25,40),anti_aliasing=True)
    tab_num_sudoku1.append((img,int(f.name[0])))


num_sudoku2 = data_test / 'Sudoku2' / 'num'
tab_num_sudoku2 = []
for f in num_sudoku2.glob("*.jpg"):
    img = rotate(rgb2gray(img_as_float(io.imread(f))),90,resize=True)
    img = resize(img,(25,40),anti_aliasing=True)
    #img = resize((img - np.mean(img))/np.std(img),(25,40),anti_aliasing=True)
    tab_num_sudoku2.append((img,int(f.name[0])))

# Accéder au chiffre tab_num_sudoko[x][0]
# Accéder au label tab_num_sudoko[x][1]

plot_4num(tab_num_sudoku1, 2, 1)
plot_num(tab_num,2)

test = correlate_img_FFT(tab_num[4],tab_num)

# test_correlate_num(tab_num_sudoku1, tab_num)

# test1 = seuillage(tab_num_sudoku1[0][0])
# test2 = seuillage(tab_num[0])

# plt.figure(1)
# plt.imshow(tab_num_sudoku1[0][0],cmap = 'binary')

# plt.figure(2)
# plt.imshow(tab_num[0],'binary')
#plt.imshow(tab_num_sudoku1[0][0],cmap = 'binary')

# plt.figure(1)
# plt.plot(tab_num[0][12,:])
# plt.plot(tab_num_sudoku1[0][0][12,:])
# plt.plot(tab_num_sudoku2[0][0][12,:])

# plt.figure(2)
# plt.plot(tab_num[0][:,20])
# plt.plot(tab_num_sudoku1[0][0][:,20])
# plt.plot(tab_num_sudoku2[0][0][:,20])