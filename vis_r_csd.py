


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

import mne


# Define subject paths
subjects_dir = '/media/white/EXT_4T/DATA/LAB/resting'
subject = 'sub-B9T21173'

# Plot and visually inspect surfaces
mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir, brain_surfaces='pial', orientation='coronal')