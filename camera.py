import rawpy
import imageio
import numpy as np
import sys
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

image = 'images/dayroom.dng'
raw = rawpy.imread(image)

# You will see RGBG for the images I provided.
print(raw.color_desc)

# You will see 4095 for the images I provided. This indicates that each pixel in the RAW images is represented as a
# 10-bit unsigned integer. You will need to map it to a 8-bit value to generate an output image.
print(raw.white_level)

# raw_img is a np array
raw_img = raw.raw_image

# You will see (3024, 4032) for the images I provided, which is the resolution of the images.
print(raw_img.shape)

# This loop will iterate overall all the pixels in the RAW image and print the RAW pixel values.
# for row in range(raw_img.shape[0]):
#     for col in range(raw_img.shape[1]):
#         print(raw_img[row, col])
