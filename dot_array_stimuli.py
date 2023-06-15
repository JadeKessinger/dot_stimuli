import os
import random
from PIL import Image, ImageDraw
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from math import sqrt, atan, radians, sin, cos, pi

# Loses a little precision when converting to ints
# TODO see if we can set is_upscaled to true for sRGBColor
def lab_to_rgb(lab):
    # Create LabColor object
    lab_color = LabColor(lab[0], lab[1], lab[2])

    # Convert Lab to sRGB
    rgb_color = convert_color(lab_color, sRGBColor)

    # Return RGB values
    return (int(rgb_color.rgb_r * 255), int(rgb_color.rgb_g * 255), int(rgb_color.rgb_b * 255))

# Calculates the new color isoluminant in CIELAB color space with based on some degree difference
def new_color(lab_color, degrees):
    # Calculate radius of circle
    radius = sqrt(lab_color[1]**2 + lab_color[2]**2)

    # Calculate new angle
    if lab_color[1] == 0:
        angle = radians(degrees)
    else:
        angle = (atan(float(lab_color[2]) / lab_color[1]) + radians(degrees)) % (2*pi)

    # Calculate new point
    a =  radius * cos(angle)
    b = radius * sin(angle)

    # Return CIELAB color
    return (lab_color[0], a, b)


# Set parameters
# TODO Width = 1024, Height = 768
image_size = 500
batch_size = 20
background_color = lab_to_rgb((50, 0, 0))
dot_radius_4 = 60
dot_radius_9 = 60
dot_radius_16 = 60
color_diff = 60 # in degrees
jitter_offset_4 = 5
jitter_offset_9 = 5

# Create the dot_arrays folder if it doesn't exist
os.makedirs("dot_arrays", exist_ok=True)

# Create the stimuli, tmaps, and dmaps folders within dot_arrays
stimuli_folder = os.path.join("dot_arrays", "stimuli")
tmaps_folder = os.path.join("dot_arrays", "tmaps")
dmaps_folder = os.path.join("dot_arrays", "dmaps")
os.makedirs(stimuli_folder, exist_ok=True)
os.makedirs(tmaps_folder, exist_ok=True)
os.makedirs(dmaps_folder, exist_ok=True)

# Generate images with 4 dots, 9 dots, and 16 dots
for i in range(batch_size):
    # Create a new image with the given size and background color
    image_4 = Image.new("RGB", (image_size, image_size), background_color)
    draw_4 = ImageDraw.Draw(image_4)

    image_9 = Image.new("RGB", (image_size, image_size), background_color)
    draw_9 = ImageDraw.Draw(image_9)

    image_16 = Image.new("RGB", (image_size, image_size), background_color)
    draw_16 = ImageDraw.Draw(image_16)

    # Draw dots for 4 dots
    center_x_4 = image_size // 2
    center_y_4 = image_size // 2

    dot_color_4_lab = (
        50,
        random.randint(-128, 128),
        random.randint(-128, 128),
    )
    special_dot_color_4_lab = new_color(dot_color_4_lab, color_diff)
    dot_color_4 = lab_to_rgb(dot_color_4_lab)
    special_dot_color_4 = lab_to_rgb(special_dot_color_4_lab)
    special_dot_index_4 = random.randint(0, 3)
    distance_4 = (image_size - 2 * dot_radius_4) // 4
    dot_coordinates_4 = [
        (
            center_x_4
            - distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
            center_y_4
            - distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
        ),
        (
            center_x_4
            + distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
            center_y_4
            - distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
        ),
        (
            center_x_4
            - distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
            center_y_4
            + distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
        ),
        (
            center_x_4
            + distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
            center_y_4
            + distance_4
            + random.randint(-jitter_offset_4, jitter_offset_4),
        ),
    ]
    for j, dot in enumerate(dot_coordinates_4):
        fill_color = dot_color_4 if j != special_dot_index_4 else special_dot_color_4
        draw_4.ellipse(
            (
                dot[0] - dot_radius_4,
                dot[1] - dot_radius_4,
                dot[0] + dot_radius_4,
                dot[1] + dot_radius_4,
            ),
            fill=fill_color,
            outline=fill_color,
        )

    # Draw dots for 9 dots
    center_x_9 = image_size // 2
    center_y_9 = image_size // 2
    dot_color_9_lab = (
        50,
        random.randint(-128, 128),
        random.randint(-128, 128),
    )
    special_dot_color_9_lab = new_color(dot_color_9_lab, color_diff)
    dot_color_9 = lab_to_rgb(dot_color_9_lab)
    special_dot_color_9 = lab_to_rgb(special_dot_color_9_lab)
    special_dot_index_9 = random.randint(0, 8)
    distance_9 = (image_size - 2 * dot_radius_9) // 2.5
    dot_coordinates_9 = [
        (
            center_x_9 - distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 - distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 - distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 + distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 - distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 - distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 + distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 - distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 + distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 + distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
        (
            center_x_9 + distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
            center_y_9 + distance_9 + random.randint(-jitter_offset_9, jitter_offset_9),
        ),
    ]
    for j, dot in enumerate(dot_coordinates_9):
        fill_color = dot_color_9 if j != special_dot_index_9 else special_dot_color_9
        draw_9.ellipse(
            (
                dot[0] - dot_radius_9,
                dot[1] - dot_radius_9,
                dot[0] + dot_radius_9,
                dot[1] + dot_radius_9,
            ),
            fill=fill_color,
            outline=fill_color,
        )

    # Draw dots for 16 dots
    center_x_16 = image_size // 2
    center_y_16 = image_size // 2
    dot_color_16 = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    special_dot_color_16 = (
        min(dot_color_16[0] + random.randint(-50, 50), 255),
        min(dot_color_16[1] + random.randint(-50, 50), 255),
        min(dot_color_16[2] + random.randint(-50, 50), 255),
    )
    special_dot_index_16 = random.randint(0, 15)
    distance_16 = (image_size - dot_radius_16) // 5
    jitter_offset_16 = dot_radius_16 // 4
    dot_coordinates_16 = []
    for row in range(4):
        for col in range(4):
            x = (
                center_x_16
                - distance_16 * 1.5
                + col * distance_16
                + random.randint(-jitter_offset_16, jitter_offset_16)
            )
            y = (
                center_y_16
                - distance_16 * 1.5
                + row * distance_16
                + random.randint(-jitter_offset_16, jitter_offset_16)
            )
            dot_coordinates_16.append((x, y))
    for j, dot in enumerate(dot_coordinates_16):
        fill_color = dot_color_16 if j != special_dot_index_16 else special_dot_color_16
        draw_16.ellipse(
            (
                dot[0] - dot_radius_16,
                dot[1] - dot_radius_16,
                dot[0] + dot_radius_16,
                dot[1] + dot_radius_16,
            ),
            fill=fill_color,
            outline=fill_color,
        )

    # Save the images with colored dots for 4 dots, 9 dots, and 16 dots
    stimuli_image_path_4 = os.path.join(stimuli_folder, f"stimulus_{i+1}_4dots.png")
    image_4.save(stimuli_image_path_4)

    stimuli_image_path_9 = os.path.join(stimuli_folder, f"stimulus_{i+1}_9dots.png")
    image_9.save(stimuli_image_path_9)

    stimuli_image_path_16 = os.path.join(stimuli_folder, f"stimulus_{i+1}_16dots.png")
    image_16.save(stimuli_image_path_16)

    # Create a new image with a black background for tmaps
    black_image_tmaps_4 = Image.new("RGB", (image_size, image_size), (0, 0, 0))
    black_draw_tmaps_4 = ImageDraw.Draw(black_image_tmaps_4)

    black_image_tmaps_9 = Image.new("RGB", (image_size, image_size), (0, 0, 0))
    black_draw_tmaps_9 = ImageDraw.Draw(black_image_tmaps_9)

    black_image_tmaps_16 = Image.new("RGB", (image_size, image_size), (0, 0, 0))
    black_draw_tmaps_16 = ImageDraw.Draw(black_image_tmaps_16)

    # Draw a white dot on the black background for tmaps at the same position as the special dot for 4 dots
    black_draw_tmaps_4.ellipse(
        (
            dot_coordinates_4[special_dot_index_4][0] - dot_radius_4,
            dot_coordinates_4[special_dot_index_4][1] - dot_radius_4,
            dot_coordinates_4[special_dot_index_4][0] + dot_radius_4,
            dot_coordinates_4[special_dot_index_4][1] + dot_radius_4,
        ),
        fill=(255, 255, 255),
        outline=(255, 255, 255),
    )

    # Draw a white dot on the black background for tmaps at the same position as the special dot for 9 dots
    black_draw_tmaps_9.ellipse(
        (
            dot_coordinates_9[special_dot_index_9][0] - dot_radius_9,
            dot_coordinates_9[special_dot_index_9][1] - dot_radius_9,
            dot_coordinates_9[special_dot_index_9][0] + dot_radius_9,
            dot_coordinates_9[special_dot_index_9][1] + dot_radius_9,
        ),
        fill=(255, 255, 255),
        outline=(255, 255, 255),
    )

    # Draw white dots on the black background for tmaps at the same position as the dots for 16 dots
    for j, dot in enumerate(dot_coordinates_16):
        if j != special_dot_index_16:
            black_draw_tmaps_16.ellipse(
                (
                    dot[0] - dot_radius_16,
                    dot[1] - dot_radius_16,
                    dot[0] + dot_radius_16,
                    dot[1] + dot_radius_16,
                ),
                fill=(255, 255, 255),
                outline=(255, 255, 255),
            )

    # Save the black and white images for tmaps
    tmaps_image_path_4 = os.path.join(tmaps_folder, f"tmap_{i+1}_4dots.png")
    black_image_tmaps_4.save(tmaps_image_path_4)

    tmaps_image_path_9 = os.path.join(tmaps_folder, f"tmap_{i+1}_9dots.png")
    black_image_tmaps_9.save(tmaps_image_path_9)

    tmaps_image_path_16 = os.path.join(tmaps_folder, f"tmap_{i+1}_16dots.png")
    black_image_tmaps_16.save(tmaps_image_path_16)

    # Create a new image with a black background for dmaps
    black_image_dmaps_4 = Image.new("RGB", (image_size, image_size), (0, 0, 0))
    black_draw_dmaps_4 = ImageDraw.Draw(black_image_dmaps_4)

    black_image_dmaps_9 = Image.new("RGB", (image_size, image_size), (0, 0, 0))
    black_draw_dmaps_9 = ImageDraw.Draw(black_image_dmaps_9)

    black_image_dmaps_16 = Image.new("RGB", (image_size, image_size), (0, 0, 0))
    black_draw_dmaps_16 = ImageDraw.Draw(black_image_dmaps_16)

    # Draw white dots on the black background for dmaps at the same position as the dots for 4 dots
    for j, dot in enumerate(dot_coordinates_4):
        if j != special_dot_index_4:
            black_draw_dmaps_4.ellipse(
                (
                    dot[0] - dot_radius_4,
                    dot[1] - dot_radius_4,
                    dot[0] + dot_radius_4,
                    dot[1] + dot_radius_4,
                ),
                fill=(255, 255, 255),
                outline=(255, 255, 255),
            )

    # Draw white dots on the black background for dmaps at the same position as the dots for 9 dots
    for j, dot in enumerate(dot_coordinates_9):
        if j != special_dot_index_9:
            black_draw_dmaps_9.ellipse(
                (
                    dot[0] - dot_radius_9,
                    dot[1] - dot_radius_9,
                    dot[0] + dot_radius_9,
                    dot[1] + dot_radius_9,
                ),
                fill=(255, 255, 255),
                outline=(255, 255, 255),
            )

    # Draw white dots on the black background for dmaps at the same position as the dots for 16 dots
    for j, dot in enumerate(dot_coordinates_16):
        if j != special_dot_index_16:
            black_draw_dmaps_16.ellipse(
                (
                    dot[0] - dot_radius_16,
                    dot[1] - dot_radius_16,
                    dot[0] + dot_radius_16,
                    dot[1] + dot_radius_16,
                ),
                fill=(255, 255, 255),
                outline=(255, 255, 255),
            )

    # Save the black and white images for dmaps
    dmaps_image_path_4 = os.path.join(dmaps_folder, f"dmap_{i+1}_4dots.png")
    black_image_dmaps_4.save(dmaps_image_path_4)

    dmaps_image_path_9 = os.path.join(dmaps_folder, f"dmap_{i+1}_9dots.png")
    black_image_dmaps_9.save(dmaps_image_path_9)

    dmaps_image_path_16 = os.path.join(dmaps_folder, f"dmap_{i+1}_16dots.png")
    black_image_dmaps_16.save(dmaps_image_path_16)
