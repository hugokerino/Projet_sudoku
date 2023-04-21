import pathlib



from code_grid import utils
from code_grid import rotate_image
from code_grid import detect_grid
from code_grid import get_cases

def read_grid(img,taille_case) : 
    theta = rotate_image.find_rotation(img,0)
    rotated = rotate_image.rotate(img,0)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    grid = get_cases.getcases(rotated,coord,taille_case)
    
    return grid,theta

def get_coordinates_cases(img):
    rotated = rotate_image.rotate(img,0)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    coordx = coord[0,:]
    coordy=coord[1,:]
    
    res = [(i,j) for i in coordx for y in coordy]
    res.reshape((2,9,9))
    return res
    


    
    
    
    
