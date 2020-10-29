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

# print(raw.postprocess()[0, 0])
# print(raw.postprocess()[0, 2])


def linear(white_level_12):  # linear tone mapping from 4096 to 256
    return 256 * white_level_12 / 4096


def pow_map(white_level_12):  # power mapping
    return pow(white_level_12, 8 / 12)


width = raw_img.shape[0]
height = raw_img.shape[1]

width = 1500
height = 1500

output_rgb = np.full((width, height, 3), np.uint8(0))

for row in range(width):
    for col in range(height):
        if raw.raw_color(row, col) == 0:
            # print("R", end=" ")
            output_rgb[row, col, 0] = pow_map(raw_img[row, col])  # R
            if row == 0:
                if col == 0:
                    output_rgb[row, col, 1] = pow_map((raw_img[row, col + 1] + raw_img[row + 1, col]) / 2)  # G
                    output_rgb[row, col, 2] = pow_map(raw_img[row + 1, col + 1])  # B
                else:
                    output_rgb[row, col, 1] = pow_map(
                        (raw_img[row, col - 1] +
                         raw_img[row, col + 1] +
                         raw_img[row + 1, col]) / 3)  # G
                    output_rgb[row, col, 2] = pow_map(
                        (raw_img[row + 1, col - 1] +
                         raw_img[row + 1, col + 1]) / 2)  # B
            elif col == 0:
                output_rgb[row, col, 1] = pow_map(  # G
                    (raw_img[row - 1, col] +
                     raw_img[row, col + 1] +
                     raw_img[row + 1, col]) / 3
                )
                output_rgb[row, col, 2] = pow_map(  # B
                    (raw_img[row - 1, col + 1] +
                     raw_img[row + 1, col + 1]) / 2
                )
            else:
                output_rgb[row, col, 1] = pow_map(  # G
                    (raw_img[row, col - 1] +
                     raw_img[row, col + 1] +
                     raw_img[row + 1, col] +
                     raw_img[row - 1, col]) / 4)
                output_rgb[row, col, 2] = pow_map(
                    (raw_img[row + 1, col - 1] +
                     raw_img[row + 1, col + 1] +
                     raw_img[row - 1, col - 1] +
                     raw_img[row - 1, col + 1]) / 4)  # B
        elif raw.raw_color(row, col) == 1:
            # print("G", end=" ")
            output_rgb[row, col, 1] = pow_map(raw_img[row, col])  # G
            if row == 0:
                if col == height - 1:
                    output_rgb[row, col, 0] = pow_map(raw_img[row, col - 1])  # R
                    output_rgb[row, col, 2] = pow_map(raw_img[row + 1, col])  # B
                else:
                    output_rgb[row, col, 0] = pow_map(
                        (raw_img[row, col - 1] +
                         raw_img[row, col + 1]) / 2)  # R
                    output_rgb[row, col, 2] = pow_map(
                        raw_img[row + 1, col])  # B
            elif col == height - 1:
                output_rgb[row, col, 0] = pow_map(raw_img[row, col - 1])  # R
                output_rgb[row, col, 2] = pow_map(
                    (raw_img[row + 1, col] +
                     raw_img[row - 1, col]) / 2)  # B
            else:
                output_rgb[row, col, 0] = pow_map(
                    (raw_img[row, col - 1] +
                     raw_img[row, col + 1]) / 2)  # R
                output_rgb[row, col, 2] = pow_map(
                    (raw_img[row - 1, col] +
                     raw_img[row + 1, col]) / 2)  # B
        elif raw.raw_color(row, col) == 2:
            # print("B", end=" ")
            output_rgb[row, col, 2] = pow_map(raw_img[row, col])  # B
            if row == width - 1:
                if col == height - 1:
                    output_rgb[row, col, 0] = pow_map(raw_img[row - 1, col - 1])  # R
                    output_rgb[row, col, 1] = pow_map(
                        (raw_img[row, col - 1] + raw_img[row - 1, col]) / 2)  # G
                else:
                    output_rgb[row, col, 0] = pow_map(
                        (raw_img[row - 1, col - 1] + raw_img[row - 1, col + 1]) / 2)  # R
                    output_rgb[row, col, 1] = pow_map(
                        (raw_img[row, col - 1] +
                         raw_img[row - 1, col] +
                         raw_img[row, col + 1]) / 3)  # G
            elif col == height - 1:
                output_rgb[row, col, 0] = pow_map(  # R
                    (raw_img[row - 1, col - 1] +
                     raw_img[row + 1, col - 1]) / 2
                )
                output_rgb[row, col, 1] = pow_map(
                    (raw_img[row - 1, col] +
                     raw_img[row + 1, col] +
                     raw_img[row, col - 1]) / 3
                )
            else:
                output_rgb[row, col, 0] = pow_map(  # R
                    (raw_img[row - 1, col - 1] +
                     raw_img[row - 1, col + 1] +
                     raw_img[row + 1, col - 1] +
                     raw_img[row + 1, col + 1]) / 4
                )
                output_rgb[row, col, 1] = pow_map(  # G
                    (raw_img[row - 1, col] +
                     raw_img[row, col + 1] +
                     raw_img[row + 1, col] +
                     raw_img[row, col - 1]) / 4
                )
        elif raw.raw_color(row, col) == 3:
            # print("G", end=" ")
            output_rgb[row, col, 1] = pow_map(raw_img[row, col])  # G
            if row == width - 1:
                if col == 0:
                    output_rgb[row, col, 2] = pow_map(raw_img[row, col + 1])  # B
                    output_rgb[row, col, 0] = pow_map(raw_img[row - 1, col])  # R
                else:
                    output_rgb[row, col, 2] = pow_map(
                        (raw_img[row, col - 1] +
                         raw_img[row, col + 1]) / 2)  # B
                    output_rgb[row, col, 0] = pow_map(
                        raw_img[row - 1, col])  # R
            elif col == 0:
                output_rgb[row, col, 2] = pow_map(raw_img[row, col + 1])  # B
                output_rgb[row, col, 0] = pow_map(
                    (raw_img[row + 1, col] +
                     raw_img[row - 1, col]) / 2)  # R
            else:
                output_rgb[row, col, 2] = pow_map(
                    (raw_img[row, col - 1] +
                     raw_img[row, col + 1]) / 2)  # B
                output_rgb[row, col, 0] = pow_map(
                    (raw_img[row - 1, col] +
                     raw_img[row + 1, col]) / 2)  # R


PIL.Image.fromarray(output_rgb, 'RGB').save('test.jpg', quality=100, optimize=False)
