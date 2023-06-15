import os
import random
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from math import sqrt, atan, radians, sin, cos, pi
from PIL import Image, ImageDraw

import setup_fldrs as fldrs


# Changes from tuple from CIELAB to RGB colorspace
# lab: tuple representing a color in the form (L, a, b)
# Note: Loses a little precision when converting to ints
# TODO see if we can set is_upscaled to true for sRGBColor
def lab_to_rgb(lab):
    # Create LabColor object
    lab_color = LabColor(lab[0], lab[1], lab[2])

    # Convert Lab to sRGB
    rgb_color = convert_color(lab_color, sRGBColor)

    # Return RGB values
    return (
        int(rgb_color.rgb_r * 255),
        int(rgb_color.rgb_g * 255),
        int(rgb_color.rgb_b * 255),
    )


# Calculates the new color isoluminant in CIELAB color space with based on some degree difference
# lab_color: tuple in the form of (L, a, b)
# degrees: number of degrees to change the color by
def new_color(lab_color, degrees):
    # Calculate radius of circle
    radius = sqrt(lab_color[1] ** 2 + lab_color[2] ** 2)

    # Calculate new angle
    if lab_color[1] == 0:
        angle = radians(degrees)
    else:
        angle = (atan(float(lab_color[2]) / lab_color[1]) + radians(degrees)) % (2 * pi)

    # Calculate new point
    a = radius * cos(angle)
    b = radius * sin(angle)

    # Return CIELAB color
    return (lab_color[0], a, b)


# Generate a list of coordinates for the dots
# array_size: the length of one side of dots for the square array
# dot_radius: radius of the dots
# jitter: pixel number for range of jitter
# width: width of the image
# height: height of the image
def generate_coords(array_size, dot_radius, jitter, width, height):
    # Calculate the center of the image
    center_x = width / 2
    center_y = height / 2

    # Calculate distances
    distance = (height - dot_radius) // array_size
    shift = (array_size - 1) * 0.5

    # Create array of coordinates
    dot_coordinates = []
    for row in range(array_size):
        for col in range(array_size):
            x = (
                center_x
                - distance * shift
                + col * distance
                + random.randint(-jitter, jitter)
            )
            y = (
                center_y
                - distance * shift
                + row * distance
                + random.randint(-jitter, jitter)
            )
            dot_coordinates.append((x, y))

    # Return list of dot coordinates
    return dot_coordinates


# Generates distractor and target colors
# color_diff: the degree difference between isoluminant distractor and target colors in CIELAB color space
# lightness: the lightness for the first parameter of CIELAB
def generate_colors(color_diff, lightness):
    dist_color_lab = (
        lightness,
        random.randint(-128, 128),
        random.randint(-128, 128),
    )
    targ_color_lab = new_color(dist_color_lab, color_diff)
    dist_color = lab_to_rgb(dist_color_lab)
    targ_color = lab_to_rgb(targ_color_lab)

    return dist_color, targ_color


# Draws one dot with the specified color and radius at the coordinate
# fill_color: color for the dots
# image: image to draw on
# dot_radius: radius of the dot
# coord: coordinate of the dot
def draw_dot(fill_color, image, dot_radius, coord):
    image.ellipse(
        (
            coord[0] - dot_radius,
            coord[1] - dot_radius,
            coord[0] + dot_radius,
            coord[1] + dot_radius,
        ),
        fill=fill_color,
        outline=fill_color,
    )


# Draws stimuli dots on the image
# dot_coordinates: a list of dot_coordinates
# dot_radius: the radius of the dot
# dist_color: the color of the distractor dots
# targ_color: the color of the target dot
# targ_index: the index of the target
# image: the ImageDraw to draw dots on
def draw_stimuli(
    dot_coordinates, dot_radius, dist_color, targ_color, targ_index, image
):
    for j, dot in enumerate(dot_coordinates):
        fill_color = dist_color if j != targ_index else targ_color
        draw_dot(fill_color, image, dot_radius, dot)


# Draws distractor dots on the image
# dot_coordinates: a list of dot_coordinates
# dot_radius: the radius of the dot
# targ_index: the index of the target
# image: the ImageDraw to draw dots on
def draw_dmap(dot_coordinates, dot_radius, targ_index, image):
    for j, dot in enumerate(dot_coordinates):
        if j != targ_index:
            draw_dot((255, 255, 255), image, dot_radius, dot)


# Creates stimuli, target map, and distractor map of a square array of distractor dots with one target dot of a different color
# array_size: the size of the search array (ex. 2 for a 2x2 array of 4 dots)
# color_diff: degree of difference in CIELAB space between isoluminant distractor and target colors
# lightness: lightness value in CIELAB color space for the image
# dot_radius: radius of the dots
# jitter: range of jitter in pixels
# width: image width
# height: image height
def draw_images(
    array_size, color_diff, lightness, dot_radius, jitter, width, height, index
):
    # Create a new image with the given background color for the stimuli
    stimuli_image = Image.new("RGB", (width, height), lab_to_rgb((lightness, 0, 0)))
    stimuli = ImageDraw.Draw(stimuli_image)

    # Create a new image for the target maps with a black background
    tmap_image = Image.new("RGB", (width, height), (0, 0, 0))
    tmap = ImageDraw.Draw(tmap_image)

    # Create a new image for the distractor maps with a black background
    dmap_image = Image.new("RGB", (width, height), (0, 0, 0))
    dmap = ImageDraw.Draw(dmap_image)

    # Generate colors, coordinates, and target dot index
    dist_color, targ_color = generate_colors(color_diff, lightness)
    dot_coordinates = generate_coords(array_size, dot_radius, jitter, width, height)
    targ_index = random.randint(0, array_size**2 - 1)

    # Draw the stimuli dots
    draw_stimuli(
        dot_coordinates, dot_radius, dist_color, targ_color, targ_index, stimuli
    )

    # Draw the target map with a white target dot
    draw_dot((255, 255, 255), tmap, dot_radius, dot_coordinates[targ_index])

    # Draw the distractor map with white distractor dots
    draw_dmap(dot_coordinates, dot_radius, targ_index, dmap)

    # Save the stimuli image
    stimuli_image_path = os.path.join(
        fldrs.stimuli_folder, f"stimulus_{array_size}dots_{index}.png"
    )
    stimuli_image.save(stimuli_image_path)

    # Save the target image
    tmaps_image_path = os.path.join(
        fldrs.tmaps_folder, f"tmap_{array_size}dots_{index}.png"
    )
    tmap_image.save(tmaps_image_path)

    # Save the distractor image
    dmaps_image_path = os.path.join(
        fldrs.dmaps_folder, f"dmap_{array_size}dots_{index}.png"
    )
    dmap_image.save(dmaps_image_path)
