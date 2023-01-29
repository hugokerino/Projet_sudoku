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
from skimage.transform import resize
from skimage.morphology import erosion, dilation 

from reco_num import plot_num, shift_img, correlate_img,correlate_img_FFT,gradient_morphology,test_correlate 


#Load data test
data_test = Path().cwd() / 'data' / 'data_test'

num_sudoku1 = data_test / 'Sudoku1' / 'num'
tab_num_sudoku1 = []
for f in num_sudoku1.glob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f)))
    img = resize((img - np.mean(img))/np.std(img),(25,40),anti_aliasing=True)
    tab_num_sudoku1.append((img,f.name[0]))


num_sudoku2 = data_test / 'Sudoku2' / 'num'
tab_num_sudoku2 = []
for f in num_sudoku2.glob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f)))
    img = resize((img - np.mean(img))/np.std(img),(25,40),anti_aliasing=True)
    tab_num_sudoku2.append((img,f.name[0]))

imgtest = rgb2gray(img_as_float(io.imread(num_sudoku1 / '2.jpg')))
plt.imshow(imgtest,cmap='binary')