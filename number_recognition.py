# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 18:30:00 2023

@author: hugob

"""

import numpy as np
from pathlib import Path
import random
import scipy.signal
from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray
from skimage.transform import resize, rotate
from skimage import filters
from matplotlib import pyplot as plt

#Functions
def img_is_empty(img):
    if (np.mean(filters.sobel(img))) < 0.01 : return True
    else : return False


def find_orientation(tab_num_to_reco, tab_num_model):
    possible_orientation = [0,90,180,270]
    tab_orientation = []
    
    for i in range(len(tab_num_to_reco)):
        if (img_is_empty(tab_num_to_reco[i][0]) == True) : 
            continue
            
        max_inter_corr = 0
    
        for k in range(len(tab_num_model)):
            inter_corr = scipy.signal.correlate(tab_num_to_reco[i][0],tab_num_model[k][0],mode = 'same',method='fft') 
            test = np.max(inter_corr)
            if test > max_inter_corr :
                max_inter_corr = test
                orientation = tab_num[k][2]
        tab_orientation.append(orientation)
        
    nbr_occurence = (tab_orientation.count(0),tab_orientation.count(90),tab_orientation.count(180),tab_orientation.count(270))
    orientation_f = possible_orientation[nbr_occurence.index(max(nbr_occurence))]
    print(f"Orientation = {orientation_f}")
    return orientation_f


def number_recognition(tab_num_to_reco, tab_num_model, orientation):
    tab_error = []
    count_passed = 0
    possible_orientation = [0,90,180,270]
    
    for i in range(len(tab_num_to_reco)):
        if (img_is_empty(tab_num_to_reco[i][0]) == True) : 
            if (0 == tab_num_to_reco[i][1] ):
                count_passed += 1
                print(f"num = vide; label = {tab_num_to_reco[i][1]} passed ")
            continue
        
        max_inter_corr = 0
        for k in range(possible_orientation.index(orientation),len(tab_num_model),4):
            inter_corr = scipy.signal.correlate(tab_num_to_reco[i][0],tab_num_model[k][0],mode = 'same',method='fft') 
            test = np.max(inter_corr)
            if test > max_inter_corr :
                num = tab_num[k][1]
                max_inter_corr = test
        if (num == tab_num_to_reco[i][1] ):
            count_passed += 1
            print(f"num = {num}; label = {tab_num_to_reco[i][1]} passed ")
        else :
            tab_error.append((num,tab_num_to_reco[i][1]))
            print(f"num = {num}; label = {tab_num_to_reco[i][1]} failed")

    print(f"Score = {count_passed*100/len(tab_num_to_reco)}%")

    if (count_passed != len(tab_num_to_reco)):
        print(f"Confusion beetwen : {tab_error}")


def plot_num_model(tab_model,i):
    plt.figure(i)
    z = 1
    for k in range(0,36,4):
        plt.subplot(3,3,z)
        plt.imshow(tab_model[k][0],cmap='binary')
        plt.title(str(k))
        z+=1
        
def plot_9nums_test(tab_num_test,i):
    len_ = len(tab_num_test)-1
    plt.figure(i)
    for i in range(9):
        k = random.randint(0,len_)
        plt.subplot(3,3,i+1)
        plt.imshow(tab_num_test[k][0],cmap='binary')
        plt.title(str(tab_num_test[k][1]))



    
#Global parameters
x_resize = 30
y_resize = 30
sudoku_test = 'Sudoku2'

#Import data reference
data = Path().cwd() / 'data' / 'data_train' / 'num'
k = 1
tab_num = []
for f in data.rglob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize((img - np.mean(img))/np.std(img),(x_resize,y_resize),anti_aliasing=True) #Standardization
    tab_num.append((img,k,0)) # Reference images
    tab_num.append((rotate(img,90),k,90))
    tab_num.append((rotate(img,180),k,180))
    tab_num.append((rotate(img,270),k,270))
    k += 1


#Import data test
data_test = Path().cwd() / 'data' / 'data_test' 
num_sudoku1 = data_test / sudoku_test / 'num'
tab_num_sudoku1 = []
for f in num_sudoku1.glob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f)))
    img = resize(img ,(x_resize,y_resize),anti_aliasing=True)
    tab_num_sudoku1.append((img,int(f.name[0])))

#Plot
plot_num_model(tab_num, 1)
plot_9nums_test(tab_num_sudoku1, 2)

#Test algo
orientation = find_orientation(tab_num_sudoku1,tab_num)
number_recognition(tab_num_sudoku1, tab_num, orientation)
