# -*- coding: utf-8 -*-
"""
Code reconnaissance de chiffre

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

def plot_4num(imgs,start,i):
    plt.figure(i)
    for i in range(4):
        plt.subplot(2,2,i+1)
        plt.imshow(imgs[start+i][0],cmap='binary')
        plt.title(str(imgs[start+i][1]))
        
def stat_img(img):
    print(f"Mean of image = {np.mean(img)}")
    print(f"Max of image = {np.max(img)}")
    print(f"Min of image = {np.min(img)}")
    
              
def seuillage(img):
    mean = np.mean(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] > mean:
               img[i,j] = 1
            else :
                img[i,j] = 0
    return img

    
def shift_img(img,shifting):
    img_shifted = np.copy(img)
    for i in range(0,img.shape[0]-shifting):
        for j in range(0,img.shape[1]-shifting):
            img_shifted[i+shifting,j+shifting] = img[i,j]
    return img_shifted

def correlate_img(img,tab_img):
    max_test = 0
    for i in range(len(tab_img)):
        test = scipy.ndimage.correlate(img,tab_img[i],mode='constant', cval=0)
        if np.max(test) > max_test :
            num = i
            max_test = np.max(test)
    return num

def correlate_img_FFT(img,tab_img):
    max_test = 0
    for i in range(len(tab_img)):
        #test = np.abs(np.fft.ifft2(np.fft.fft2(img)*np.fft.fft2(tab_img[i])))    
        test = scipy.signal.correlate(img,tab_img[i],method='fft')
        if np.max(test) > max_test :
            num = i+1
            max_test = np.max(test)
    return num

def gradient_morphology(img):
    return dilation(img)-erosion(img)

def test_correlate(tab_img_to_reco,tab_img_data):
    count_passed = 0
    tab_failed = []
    for i in range(len(tab_img_to_reco)):
        num = correlate_img_FFT(tab_img_to_reco[i],tab_img_data)
        if num == i+1:
            print(f"{i} Passed")
            count_passed += 1
        else:
            print("Failed")
            tab_failed.append((i,num))
            
    test_score = count_passed/len(tab_img_to_reco)
    print(f"Test score = {test_score}")
    if count_passed != len(tab_img_to_reco):
          print(f"Confusion beetwen (label,reconnu) : \n {tab_failed}\n")

# tab_img_to_reco : tab of number to detect
# tab_img_data : tab of reference number
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
    print(f"Test score = {test_score}")
    if count_passed != len(tab_img_to_reco):
          print(f"Confusion beetwen (label,reconnu) : \n {tab_failed}\n")

    
                 
#Import data
data = Path().cwd() / 'data' / 'num_police1'

tab_num = []
tab_num_blurred = []
tab_num_shift = []
tab_num_shift_blurred = []

for f in data.rglob("*.jpg"):        
    img = rgb2gray(img_as_float(io.imread(f))) #Normalization
    img = resize((img - np.mean(img))/np.std(img),(25,40),anti_aliasing=True) #Standardization
    tab_num.append(img) # Reference images
    tab_num_blurred.append(filters.gaussian(img,0.5)) #Blurred with Gaussian filter
    tab_num_shift.append(shift_img(img,5)) #Shifting the image
    tab_num_shift_blurred.append(filters.gaussian(tab_num_shift[-1],0.5)) # Filtered and shifting



#Plot data imported
plot_num(tab_num,1)
plot_num(tab_num_blurred,2)
plot_num(tab_num_shift,3)
plot_num(tab_num_shift_blurred,4)

# Test algo recognition
print("Test with blurred number")
test_correlate(tab_num_blurred,tab_num)

print("Test with shifted number")
test_correlate(tab_num_shift,tab_num)

print("Test with shifted and blurred number")
test_correlate(tab_num_shift_blurred,tab_num)


# test = np.abs(np.fft.ifft2(np.fft.fft2(tab_num[0])*np.fft.fft2(tab_num[0])))
# test2 = scipy.ndimage.correlate(tab_num[0],tab_num[0],mode='constant', cval=0)
# test3 = scipy.signal.correlate(tab_num[0],tab_num[0],method='fft')

# arg1 = np.unravel_index(np.argmax(test, axis=None), test.shape)
# arg2 = np.unravel_index(np.argmax(test2, axis=None), test2.shape)
# arg3 = np.unravel_index(np.argmax(test3, axis=None), test3.shape)



