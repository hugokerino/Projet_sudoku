# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:57:30 2023

@author: hugob
"""

import numpy as np
from pathlib import Path

from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray
from skimage.transform import resize, rotate

from functions import plot_num, plot_4num, test_correlate_num
          
#Import data reference
data = Path().cwd() / 'data' / 'data_train' / 'num'

x_resize = 30
y_resize = 40

tab_num = []
for f in data.rglob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize((img - np.mean(img))/np.std(img),(x_resize,y_resize),anti_aliasing=True) #Standardization
    tab_num.append(img) # Reference images
   
    
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
    
num_sudoku3 = data_test / 'Sudoku1' / 'num'    
tab_num_sudoku3 = []
for f in num_sudoku3.glob("*.jpg"):
    img = rotate(rgb2gray(img_as_float(io.imread(f))),90)
    img = resize(img,(x_resize,y_resize),anti_aliasing=True)
    tab_num_sudoku3.append((img,int(f.name[0])))

num_sudoku4 = data_test / 'Sudoku1' / 'num'    
tab_num_sudoku4 = []
for f in num_sudoku4.glob("*.jpg"):
    img = rotate(rgb2gray(img_as_float(io.imread(f))),90)
    img = resize(img,(x_resize,y_resize),anti_aliasing=True)
    tab_num_sudoku4.append((img,int(f.name[0])))


#Plot 
plot_num(tab_num,1)
plot_4num(tab_num_sudoku1, 2)
plot_4num(tab_num_sudoku2, 3)
plot_4num(tab_num_sudoku3, 4)
plot_4num(tab_num_sudoku4, 5)


#Tests
# Test number of same sudoku different acquisition
print("Test with first sudoku :")
test_correlate_num(tab_num_sudoku1,tab_num)
# Test number of different sudoku
print("Test with second sudoku :")
test_correlate_num(tab_num_sudoku2,tab_num)
# Test number of different sudoku
print("Test with third sudoku :")
test_correlate_num(tab_num_sudoku3,tab_num)
# Test number of different sudoku
print("Test with fourth sudoku :")
test_correlate_num(tab_num_sudoku4,tab_num)


# from matplotlib import pyplot as plt
# from skimage.filters import threshold_otsu,try_all_threshold

# def thresholding (img):
#     test = np.copy(img)
#     thresh = threshold_otsu(test)
#     img = test > thresh
#     return img

# def stat_img(img):
#     print(f"Mean of image = {np.mean(img)}")
#     print(f"Max of image = {np.max(img)}")
#     print(f"Min of image = {np.min(img)}")


# k = 5
# test = np.copy(tab_num[k])
# # img = thresholding(test)
# # plt.subplot(2,1,1), plt.imshow(test,cmap='binary'), plt.title("before")
# # plt.subplot(2,1,2), plt.imshow(img,cmap='binary'), plt.title("after")

# fig, ax = try_all_threshold(test, figsize=(10, 6), verbose=False)