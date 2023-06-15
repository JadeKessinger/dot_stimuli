# Creates folders to store images
# Author: Jade Kessinger
# Created with the help of ChatGPT and following Prof. Wloka's Asymmetric Search stimuli generation
import os

# Create the dot_arrays folder if it doesn't exist
os.makedirs("dot_arrays", exist_ok=True)

# Create the stimuli, tmaps, and dmaps folders within dot_arrays
stimuli_folder = os.path.join("dot_arrays", "stimuli")
tmaps_folder = os.path.join("dot_arrays", "tmaps")
dmaps_folder = os.path.join("dot_arrays", "dmaps")
os.makedirs(stimuli_folder, exist_ok=True)
os.makedirs(tmaps_folder, exist_ok=True)
os.makedirs(dmaps_folder, exist_ok=True)
