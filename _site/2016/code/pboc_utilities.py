import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

import glob
import skimage.io
import skimage.measure
import skimage.filters

def bar_plot (data, n_slices, dx = 1, dy = 1, z_max = 1, x_label = 'x',
              y_label='y', z_label='z', elev_angle = 30, azim_angle = 115):
    """
    Makes a 3d bar plot of the data given as a 2d numpy array.

    Parameters
    ----------
    data: 2d-array
        Two-dimensional numpy array of z-values
    n_slices: int
        Number of 'slices' in y-directions to be used in the 3D plot
    dx: float
        Distance between neighboring x-positions
    dy: float
        Distance between neighboring y-positions
    x_label: str
        Label of the x-axis
    y_label: str
        Label of the y-axis
    z_lable: str
        Label of the z-axis
    elev_angle: int
        Alevation viewing angle
    azim_angle: int
        Azimuthal viewing angle
    z_max: float
        Default limit to the z-axis

    Returns
    -------
    fig: pyplot figure object
        Figure of the 3d-plot

    ax: pyplot axes object
        Axes object that contains the figure elements
    """

    # Initialize the figure object
    fig = plt.figure(figsize = [10, 8])
    ax = fig.add_subplot(111, projection='3d')

    # Colors to indicate variation in y-axis
    colors = sns.color_palette('YlGnBu_r', n_colors=n_slices+1)

    # Dimensions of the 2d-array
    x_length, y_length = data.shape

    # Initial index of the slice
    i_slice = 0

    # Iterate through each slice and add bar plots
    for y in np.arange(0, y_length, y_length//n_slices):

        # x-, y- and z-positions
        x_pos = np.arange(x_length)*dx
        y_pos = y*np.ones(x_length)*dy
        z_pos = np.zeros(x_length)

        # Horizontal dimensions of the bars
        delta_x = dx*np.ones(x_length)
        delta_y = 2*dy*np.ones(x_length)

        # Heights in the z-direction
        delta_z = data[:,y]

        ax.bar3d(x_pos, y_pos, z_pos, delta_x, delta_y, delta_z,
                 color = colors[i_slice])

        i_slice = i_slice + 1;

    # Add axis labels
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)

    # Adjust the 3d viewing angle of the plot
    ax.view_init(elev_angle, azim_angle)

    # Set the z-limit of the plot
    z_max = np.min([z_max, np.max(data)])
    ax.set_zlim([0, z_max])

    return fig, ax


def create_mask (phase_image, gauss_radius = 50, threshold = -0.2, \
                 pixel_size = 0.16, area_low = 1, area_high = 5):

    # Normalize
    im_float = (phase_image - np.min(phase_image))/(np.max(phase_image)-np.min(phase_image))

    # Find the background
    im_bg = skimage.filters.gaussian(im_float, gauss_radius)

    # Subtract the background
    im_gauss = im_float - im_bg

    # Threshold the image
    im_thresh = im_gauss < threshold

    # Label the image
    im_label = skimage.measure.label(im_thresh)

    # Obtain the features of the objects
    props = skimage.measure.regionprops(im_label)

    # Remove small objects
    im_mask = np.zeros_like(im_label)
    for prop in props:
        area = prop.area * pixel_size**2
        if (area > area_low) and (area < area_high):
            im_mask = im_mask + (im_label == prop.label)

    # Label the mask
    im_mask_label = skimage.measure.label(im_mask)

    # Return the labeled mask
    return im_mask_label


def find_intensities (im_yfp, im_mask_label):

    # List to store the object intensity values
    intensities = []

    # Obtain the features of objects in the YFP channel
    props = skimage.measure.regionprops(im_mask_label, intensity_image=im_yfp)

    # Add the YFP intensity values
    for prop in props:
        intensities.append(prop.mean_intensity)

    return intensities


def find_intensities_all (operator, repressor):
    # Array to store intensity values from all the strains
    intensities_all = []

    # Filename structure
    file_structure_phase = 'data/lacI_titration/' + operator + '_' + repressor + '_' + 'phase*'
    file_structure_yfp = 'data/lacI_titration/' + operator + '_' + repressor + '_' + 'yfp*'

    # Name of all images for a given strain
    phase_names = glob.glob(file_structure_phase)
    yfp_names = glob.glob(file_structure_yfp)

    # Number of positions
    n_positions = len(phase_names)

    for i in range(n_positions):
        im_phase = skimage.io.imread(phase_names[i])
        im_yfp = skimage.io.imread(yfp_names[i])

        im_mask_label = create_mask(im_phase)
        intensities = find_intensities(im_yfp, im_mask_label)

        for intensity in intensities:
            intensities_all.append(intensity)

    return intensities_all
