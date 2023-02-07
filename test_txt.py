# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:10:17 2023

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

plt.close()
data = Path().cwd() / 'data' / 'data_test' / 'Sudoku4'/ 'sudoku_complete' / '73.jpg'
img8 =  rgb2gray(img_as_float(io.imread(data))) #Normalization
plt.figure(1)
plt.imshow(img8)
img8 = filters.sobel(img8)
plt.figure(2)
plt.imshow(img8)