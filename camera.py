import rawpy
import imageio
import PIL
import numpy as np
import sys
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

image = 'images/dayroom.dng'
raw = rawpy.imread(image)

# You will see RGBG for the images I provided.
# print(raw.color_desc)

# You will see 4095 for the images I provided. This indicates that each pixel in the RAW images is represented as a
# 10-bit unsigned integer. You will need to map it to a 8-bit value to generate an output image.
# print(raw.white_level)

# raw_img is a np array
raw_img = raw.raw_image


# You will see (3024, 4032) for the images I provided, which is the resolution of the images.
# print(raw_img.shape)

# This loop will iterate overall all the pixels in the RAW image and print the RAW pixel values.
# for row in range(raw_img.shape[0]):
#     for col in range(raw_img.shape[1]):
#         print(raw_img[row, col])

print(raw.postprocess()[0, 0])
print(raw.postprocess()[0, 2])



def linear_map(white_level_12):  # linear tone mapping from 4096 to 256
    return 256 * white_level_12 / 4096


output_rgb = np.full((10, 10, 3), 0)

for row in range(10):
    for col in range(10):
        if raw.raw_color(row, col) == 0:
            # print("R", end=" ")
            output_rgb[row, col, 0] = linear_map(raw_img[row, col])  # R
            if row == 0:
                if col == 0:
                    output_rgb[row, col, 1] = linear_map((raw_img[row, col + 1] + raw_img[row + 1, col]) / 2)  # G
                    output_rgb[row, col, 2] = linear_map(raw_img[row + 1, col + 1])  # B
                else:
                    output_rgb[row, col, 1] = linear_map(
                        (raw_img[row, col - 1] +
                         raw_img[row, col + 1] +
                         raw_img[row + 1, col]) / 3)  # G
                    output_rgb[row, col, 2] = linear_map(
                        (raw_img[row + 1, col - 1] +
                         raw_img[row + 1, col + 1]) / 2)  # B
            else:
                output_rgb[row, col, 1] = linear_map(   # G
                    (raw_img[row, col - 1] +
                     raw_img[row, col + 1] +
                     raw_img[row + 1, col] +
                     raw_img[row - 1, col]) / 4)
                output_rgb[row, col, 2] = linear_map(
                    (raw_img[row + 1, col - 1] +
                     raw_img[row + 1, col + 1] +
                     raw_img[row - 1, col - 1] +
                     raw_img[row - 1, col + 1]) / 4)  # B
        elif raw.raw_color(row, col) == 1:
            print("G", end=" ")
        elif raw.raw_color(row, col) == 2:
            print("B", end=" ")
        elif raw.raw_color(row, col) == 3:
            print("G", end=" ")
    print()

    print(output_rgb)
