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
     
x_resize = 30
y_resize = 30


#Import data reference
data = Path().cwd() / 'data' / 'data_train' / 'num'

k = 1
tab_num = []
for f in data.rglob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize((img - np.mean(img))/np.std(img),(x_resize,y_resize),anti_aliasing=True) #Standardization
    tab_num.append((img,k)) # Reference images
    tab_num.append((rotate(img,90),k))
    tab_num.append((rotate(img,180),k))
    tab_num.append((rotate(img,270),k))
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


#Rotate numbers
tab_num_sudoku5 = []
tab_num_sudoku6 = []
tab_num_sudoku7 = []
for k in range(len(tab_num_sudoku1)):
    tab_num_sudoku5.append((rotate(tab_num_sudoku1[k][0],90),tab_num_sudoku1[k][1]))
    tab_num_sudoku6.append((rotate(tab_num_sudoku1[k][0],180),tab_num_sudoku1[k][1]))
    tab_num_sudoku7.append((rotate(tab_num_sudoku1[k][0],270),tab_num_sudoku1[k][1]))

#Plot 
#plot_num(tab_num,1)
plot_4num(tab_num_sudoku1, 2)
plot_4num(tab_num_sudoku2, 3)
plot_4num(tab_num_sudoku3, 4)
plot_4num(tab_num_sudoku4, 5)


# plot_4num(tab_num_sudoku5, 6)
# plot_4num(tab_num_sudoku6, 7)
# plot_4num(tab_num_sudoku7, 8)



#Tests
# Test number of same sudoku different acquisition
print("Test with first sudoku :")
test_correlate_num(tab_num_sudoku1,tab_num)
#Test number of different sudoku different police
print("Test with second sudoku :")
test_correlate_num(tab_num_sudoku2,tab_num)
# # Test number of different sudoku
# print("Test with third sudoku :")
# test_correlate_num(tab_num_sudoku3,tab_num)
# #Test number of different sudoku
# print("Test with fourth sudoku :")
# test_correlate_num(tab_num_sudoku4,tab_num)


# Test number of different sudoku
print("Test with fifth sudoku rotated 90 :")
test_correlate_num(tab_num_sudoku5,tab_num)
# Test number of different sudoku
print("Test with sixth sudoku rotated 180 :")
test_correlate_num(tab_num_sudoku6,tab_num)
# Test number of different sudoku
print("Test with seventh sudoku rotated 270:")
test_correlate_num(tab_num_sudoku7,tab_num)

