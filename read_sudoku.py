# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:47:43 2023

@author: hugob
"""

import sys
sys.path.insert(1, 'code_number')
import utils
import detect_grid
import get_cases
import rotate_image

sys.path.insert(2, 'code_number')
from functions_number import import_data_model,find_orientation,number_recognition,write_sudoku


def read_grid(img, taille_case):
    theta = rotate_image.find_rotation(img,0)
    rotated = rotate_image.rotate(img,0)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    cases = get_cases.getcases(rotated,coord,taille_case) 
    return cases,theta

def find_number(cases, tab_num_model, orientation_initial, name_sudoku_text, path_to_write):
    orientation_modif = find_orientation(cases,tab_num_model)
    tab_num_find = number_recognition(cases, tab_num_model, orientation_modif)
    write_sudoku(tab_num_find,name_sudoku_text, path_to_write)
    
    return orientation_initial - orientation_modif
    


### TEST ###
from pathlib import Path
pixel_resize = 20

path_data_test = data = Path().cwd() / 'data' / 'data_test' / 'sudoku' 
path_where_write_sudoku = Path().cwd() / 'test_result_read_sudoku'
tab_num_model = import_data_model(pixel_resize)


test = '20.jpg'
img = utils.read( path_data_test  / test)
[cases,theta] = read_grid(img,pixel_resize)
orientation = find_number(cases,tab_num_model, theta, 'test',path_where_write_sudoku)


# from matplotlib import pyplot as plt
# from skimage.transform import rotate
# plt.close('all')
# plt.figure(1)
# plt.imshow(rotate(img,orientation),cmap='binary')