# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 19:13:21 2023

@author: hugob

functions used for number detection

"""

import numpy as np
import scipy.ndimage
import scipy.signal
from matplotlib import pyplot as plt
import random

# Functions

# Plot number used as references #

# imgs : table of references images
# i : number of the figure
def plot_num(imgs,i):
    plt.figure(i)
    nbr_num = len(imgs)
    for i in range(nbr_num):
        plt.subplot(5,5,i+1)
        plt.imshow(imgs[i],cmap='binary')
        plt.title(str(i))



# Plot 4 number to detect #

# imgs : table of images to detect
# i : number of the figure
def plot_4num(imgs,i):
    len_ = len(imgs)-1
    plt.figure(i)
    for i in range(4):
        k = random.randint(0,len_)
        plt.subplot(2,2,i+1)
        plt.imshow(imgs[k][0],cmap='binary')
        plt.title(str(imgs[k][1]))


# Perform cross correlation and return number detected #

#img : number to detect
#tab_img : table of references images
def correlate_img_FFT(img,tab_img):
    max_test = 0
    for i in range(len(tab_img)):
        #test = np.abs(np.fft.ifft2(np.fft.fft2(img)*np.fft.fft2(tab_img[i])))    
        test = scipy.signal.correlate(img,tab_img[i],mode = 'same',method='fft')
        if np.max(test) > max_test :
            num = i+1
            max_test = np.max(test)
    return num



# Test data number to detect#

# tab_img_to_reco : table of numbers to detect
# tab_img_data : table of references numbers
def test_correlate_num(tab_img_to_reco,tab_img_data):
    count_passed = 0
    tab_failed = []
    for i in range(len(tab_img_to_reco)):
        num = correlate_img_FFT(tab_img_to_reco[i][0],tab_img_data)
        if num == tab_img_to_reco[i][1]:
            print(f"chiffre = {tab_img_to_reco[i][1]} reconnu = {num} : Passed")
            count_passed += 1
        else:
            print(f"chiffre = {tab_img_to_reco[i][1]} reconnu = {num} : Failed")
            tab_failed.append((tab_img_to_reco[i][1],num))
            
    test_score = count_passed/len(tab_img_to_reco)
    print(f"Test score = {test_score*100}%\n")
    if count_passed != len(tab_img_to_reco):
          print(f"Confusion beetwen (label,reconnu) : \n {tab_failed}\n")

    
                 
