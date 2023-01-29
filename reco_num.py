# -*- coding: utf-8 -*-
"""
Code reconnaissance de chiffre

"""

import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
from scipy.ndimage import correlate

from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray
from skimage import filters
from skimage.transform import resize
from skimage.morphology import erosion, dilation 


# Functions
def plot_num(imgs,i):
    plt.figure(i)
    nbr_num = len(imgs)
    for i in range(nbr_num):
        plt.subplot(5,5,i+1)
        plt.imshow(imgs[i],cmap='binary')
        plt.title(str(i))
    
    
def shift_img(img,shifting):
    img_shifted = np.copy(img)
    for i in range(0,img.shape[0]-shifting):
        for j in range(0,img.shape[1]-shifting):
            img_shifted[i+shifting,j+shifting] = img[i,j]
    return img_shifted

def correlate_img(img,tab_img):
    max_test = 0
    for i in range(len(tab_img)):
        test = correlate(img,tab_img[i],mode='constant', cval=0)
        if np.max(test) > max_test :
            num = i
            max_test = np.max(test)
    return num

def correlate_img_FFT(img,tab_img):
    max_test = 0
    for i in range(len(tab_img)):
        test = np.fft.ifft2(np.fft.fft2(img)*np.fft.fft2(tab_img[i]))
        if np.max(test) > max_test :
            num = i
            max_test = np.max(test)
    return num

def gradient_morphology(img):
    return dilation(img)-erosion(img)

def test_correlate(tab_img_to_reco,tab_img_data):
    count_passed = 0
    tab_failed = []
    for i in range(len(tab_img_to_reco)):
        num = correlate_img_FFT(tab_img_to_reco[i],tab_img_data)
        if num == i:
            print("Passed")
            count_passed += 1
        else:
            print("Failed")
            tab_failed.append((i,num))
            
    test_score = count_passed/len(tab_img_to_reco)
    print(f"Test score = {test_score},\nUnable to detect = {tab_failed}\n")
    
#Import data
data = Path().cwd() / 'data' / 'num_police1'

tab_num = []
tab_num_blurred = []
tab_num_shift = []
tab_num_shift_blurred = []

for f in data.rglob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize((img - np.mean(img))/np.std(img),(50,80),anti_aliasing=True) #Standardization
    tab_num.append(img) # Reference images
    tab_num_blurred.append(filters.gaussian(img,1)) #Blurred with Gaussian filter
    tab_num_shift.append(shift_img(img,8)) #Shifting the image
    tab_num_shift_blurred.append(filters.gaussian(tab_num_shift[-1],1)) # Filtered and shifting

#Plot data imported
# plot_num(tab_num,1)
# plot_num(tab_num_blurred,2)
# plot_num(tab_num_shift,3)
# plot_num(tab_num_shift_blurred,4)

#Test algo recognition
# print("Test with blurred number")
# test_correlate(tab_num_blurred,tab_num)

# print("Test with shifted number")
# test_correlate(tab_num_shift,tab_num)

# print("Test with shifted and blurred number")
# test_correlate(tab_num_shift_blurred,tab_num)


test = np.fft.ifft2(np.fft.fft2(tab_num[0])*np.fft.fft2(tab_num[0]))
test2 = correlate(tab_num[0],tab_num[0],mode='constant', cval=0)
