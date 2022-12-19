# a python script that takes an image file and converts it to black and white boolean array. then removes islands of black pixels smaller than a threshold pixel count. 

# import the necessary modules
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.ndimage import measurements
from pathlib import Path


# prompt the user for a file name
filename = input("Enter the name of the jpeg/png file: ")
# if file name is blank use image.jpg
if filename == '':
    filename = 'image.jpg'

# Open the image using the Image module
image = Image.open(filename)

# a function that takes in an image and converts it to boolean array based on a threshold which is 50%
def img2bool(image, threshold=0.5):
    img = Image.open(image)
    img = img.convert('L')
    img = np.array(img)
    img = img / 255
    img = img > threshold
    return img

# a function to save the array as a png file
def bool2png(img, name='test.png'):
    img = Image.fromarray(img.astype(np.uint8) * 255)
    img.save(name)
# a function to save the array as a svg file (not working)
# def bool2svg(array, filename='test.svg'):
#     height, width = array.shape
#     with open(filename, 'w') as f:
#         f.write('<svg width="{}" height="{}">\n'.format(width, height))
#         # Label the connected components in the array
#         labeled_array, num_features = measurements.label(array)
#         # Iterate over the labeled components
#         for i in range(1, num_features + 1):
#             # Select the current component
#             component = labeled_array == i
#             # Initialize an empty list to store the path data
#             path_data = []
#             # Iterate over the elements of the component
#             for y in range(height):
#                 for x in range(width):
#                     if component[y,x]:
#                         # If the current element is True, add its coordinates to the path data
#                         path_data.append((x, y))
#             # If there is any path data, write a <path> element to the file
#             if path_data:
#                 f.write('<path d="M{} {}'.format(*path_data[0]))
#                 for x, y in path_data[1:]:
#                     f.write('L{} {}'.format(x, y))
#                 f.write('" fill="black"/>\n')
#         f.write('</svg>')


# test the output of the middle stage
bwimgbool = img2bool(filename)
# bool2png(bwimgbool, 'test.png')

# a function that takes in a boolean array and removes islands of white pixels smaller than a certain size
def remove_white_islands(img, min_size=1000):
    labeled_array, num_features = measurements.label(img)
    sizes = measurements.sum(img, labeled_array, range(num_features + 1))
    mask_size = sizes < min_size
    remove_pixel = mask_size[labeled_array]
    img[remove_pixel] = 0
    return img

# a function that takes in a boolean array and removes islands of black pixels smaller than a certain size
def remove_black_islands(img, min_size=1000):
    img = ~img
    labeled_array, num_features = measurements.label(img)
    sizes = measurements.sum(img, labeled_array, range(num_features + 1))
    mask_size = sizes < min_size
    remove_pixel = mask_size[labeled_array]
    img[remove_pixel] = 0
    img = ~img
    return img

minsize = 5000
cleanimgbool = remove_white_islands(remove_black_islands(bwimgbool,minsize),minsize)
bool2png(cleanimgbool, 'output.png')
# bool2svg(cleanimgbool, 'test2.svg')

# open the image on a windows machine
# import os
# os.startfile('test2.png')
# os.startfile('test2.svg')