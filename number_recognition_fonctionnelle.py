# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:30:40 2023

@author: hugob
"""

import numpy as np
import scipy.signal
from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray
from skimage import filters

from skimage.transform import resize, rotate
from pathlib import Path

#Functions
def img_is_empty(img):
    if (np.mean(filters.sobel(img))) < 0.02 : return True
    else : return False


def find_orientation(tab_num_to_reco, tab_num_model):
    possible_orientation = [0,90,180,270]
    tab_orientation = []
    
    for i in range(tab_num_to_reco.shape[0]):
        for j in range(tab_num_to_reco.shape[1]):
            if (img_is_empty(tab_num_to_reco[i,j,:,:]) == True) : 
                continue
            
            max_inter_corr = 0
    
            for k in range(len(tab_num_model)):
                inter_corr = scipy.signal.correlate(tab_num_to_reco[i,j,:,:],tab_num_model[k][0],mode = 'same',method='fft') 
                test = np.max(inter_corr)
                if test > max_inter_corr :
                    max_inter_corr = test
                    orientation = tab_num_model[k][2]
            tab_orientation.append(orientation)
        
    nbr_occurence = (tab_orientation.count(0),tab_orientation.count(90),tab_orientation.count(180),tab_orientation.count(270))
    orientation_f = possible_orientation[nbr_occurence.index(max(nbr_occurence))]
    
    return orientation_f



def number_recognition(tab_num_to_reco, tab_num_model, orientation):
    possible_orientation = [0,90,180,270]
    tab_to_return = np.zeros((tab_num_to_reco.shape[0],tab_num_to_reco.shape[1]))
    
    for i in range(tab_num_to_reco.shape[0]):
        for j in range(tab_num_to_reco.shape[1]):
            if (img_is_empty(tab_num_to_reco[i,j,:,:]) == True) :
                tab_to_return[i,j] = 0
                continue
        
            max_inter_corr = 0
            for k in range(possible_orientation.index(orientation),len(tab_num_model),4):
                inter_corr = scipy.signal.correlate(tab_num_to_reco[i,j,:,:],tab_num_model[k][0],mode = 'same',method='fft') 
                test = np.max(inter_corr)
                if test > max_inter_corr :
                    num = tab_num_model[k][1]
                    max_inter_corr = test
                    
            tab_to_return[i,j] = num
            #print(f"({i},{j}) = {num}")
    return tab_to_return


def write_sudoku(tab_num_find):
    sudoku_txt = open("sudoku.txt","w")
    
    for row in range(tab_num_find.shape[0]):
        for colum in range(tab_num_find.shape[1]):
            char = str(round(tab_num_find[row,colum]))+' '
            sudoku_txt.write(char) 
        sudoku_txt.write("\n")
    
    sudoku_txt.close()


def main_reco(tab_num_to_reco,orientation_initial):
    #Global parameters
    x_resize = 30
    y_resize = 30

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
    
    orientation_modif = find_orientation(tab_num_to_reco,tab_num)
    tab_num_find = number_recognition(tab_num_to_reco, tab_num, orientation_modif)
    write_sudoku(tab_num_find)
    
    return orientation_modif + orientation_initial



#Import data test
x_resize = 30
y_resize = 30
tab_num_test = np.zeros((6,9,x_resize,y_resize))
data_test = Path().cwd() / 'data' / 'data_test' / 'Sudoku3' / 'sudoku_complete'

for f in data_test.glob("*.jpg"):
    img = rgb2gray(img_as_float(io.imread(f)))
    img = resize(img ,(x_resize,y_resize),anti_aliasing=True)
    x, y = int(f.name[0]), int(f.name[1])
    tab_num_test[x,y] = img

result = main_reco(tab_num_test, 0)