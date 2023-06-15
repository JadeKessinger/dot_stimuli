# Batch processing using create_stimuli.py for making datasets of color dot stimuli
# Author: Jade Kessinger
# Created with the help of ChatGPT and following Prof. Wloka's Asymmetric Search stimuli generation
import create_stimuli as cstm

# Set parameters
image_width = 1024
image_height = 768
batch_size = 20
lightness = 50  # in CIELAB color space
color_diff = 60  # in degrees
dot_radius = 60  # in pixels
jitter = 10  # in pixels

# Generate images with 4 dots, 9 dots, and 16 dots
for i in range(batch_size):
    cstm.draw_images(
        2, color_diff, lightness, dot_radius, jitter, image_width, image_height, i + 1
    )
    cstm.draw_images(
        3, color_diff, lightness, dot_radius, jitter, image_width, image_height, i + 1
    )
    cstm.draw_images(
        4, color_diff, lightness, dot_radius, jitter, image_width, image_height, i + 1
    )
