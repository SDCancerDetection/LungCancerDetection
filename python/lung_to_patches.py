import SimpleITK
import numpy as np
import os
import scipy.ndimage
import matplotlib.pyplot as plt

# Constants
PATCH_WIDTH = 64          # This is the number of pixels wanted in the final patch
SLIDE_INCREMENT = 32       # Pixels to move sliding window between each patch
directory = "E:\\Fall 2018\\EE4901\\CancerDetectionProgram\\Data\\test"


def load_itk_image(filename):
    itk_image = SimpleITK.ReadImage(filename)

    numpy_image = SimpleITK.GetArrayFromImage(itk_image)
    numpy_origin = np.array(list(reversed(itk_image.GetOrigin())))
    numpy_spacing = np.array(list(reversed(itk_image.GetSpacing())))

    return numpy_image, numpy_origin, numpy_spacing


# Takes 3D image and resample to make the spacing between pixels equal to "new_spacing"
def resample(image, spacing):
    new_spacing = [1, 1, 1]
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
    return image, new_spacing


def normalize_planes(npz_array):
    max_hu = 400
    min_hu = -1000

    npz_array = (npz_array - min_hu) / (max_hu - min_hu)
    npz_array[npz_array > 1] = 1.
    npz_array[npz_array < 0] = 0.
    return npz_array


# Show the plot of the image
def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.show()


# Given the file path to the image, search the CSV for any nodules that are related to that scan and display them.
def get_patches(filepath):
    numpy_image, numpy_origin, numpy_spacing = load_itk_image(filepath)
    numpy_image, numpy_spacing = resample(numpy_image, numpy_spacing)
    numpy_image = normalize_planes(numpy_image)             # Converts pixels to HU values

    slices, height, width = numpy_image.shape               # Get dimensions of the image
    w, h, s = 0, 0, 0                                       # Initialize loop counters to 0
    test = 0

    while s < slices:                                       # Go through each slice
        while h < height - PATCH_WIDTH:                     # Go through y dir until bottom of image slice
            while w < width - PATCH_WIDTH:                  # Go through x dir until right of image slice

                patch = numpy_image[s, h:h + PATCH_WIDTH, w:w + PATCH_WIDTH]    # Gets 64x64 pixel patch to test on
                test += 1
                # TODO - ADD the code to test on this patch for ML algorithm
                w += SLIDE_INCREMENT
            h += SLIDE_INCREMENT
            w = 0
        s += 1
        h = 0
    print(test)


# Print out the nodules for each file in the directory
for file_name in os.listdir(directory):
    file = os.path.join(directory, file_name)
    if ".mhd" in file_name:
        get_patches(file)
