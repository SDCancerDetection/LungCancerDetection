import SimpleITK
import numpy as np
import os
from PIL import Image
import csv
import scipy.ndimage
import matplotlib.pyplot as plt
import random

# Constants
PATCH_WIDTH = 64          # This is the number of pixels wanted in the final patch
SLIDE_INCREMENT = 32       # Pixels to move sliding window between each patch
#directory = "E:\\Spring 2019\\EE4910\\LungCancerDetection\\python\\subset_ex"

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
def get_patches(filepath, slice_filepath, csv_path):
    numpy_image, numpy_origin, numpy_spacing = load_itk_image(filepath)
    numpy_image, numpy_spacing = resample(numpy_image, numpy_spacing)
    numpy_image = normalize_planes(numpy_image)             # Converts pixels to HU values

    slices, height, width = numpy_image.shape               # Get dimensions of the image
    w, h, s = 0, 0, 0                                       # Initialize loop counters to 0
    test = 0
    # Open file to write csv data to for each patch
    with open(csv_path + "\\data.csv", mode='w', newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)       # Set up arguments
        while s < slices:                                       # Go through each slice
            while h < height - PATCH_WIDTH:                     # Go through y dir until bottom of image slice
                while w < width - PATCH_WIDTH:                  # Go through x dir until right of image slice

                    patch = numpy_image[s, h:h + PATCH_WIDTH, w:w + PATCH_WIDTH]    # Get 64x64 px patch for prediction
                    test = random.random()                                   # Random var for testing, replace with prediction value
                    # TODO - ADD the code to test on this patch for ML algorithm

                    # Write patch information to the CSV File
                    data_writer.writerow([w, h, s, test])
                    w += SLIDE_INCREMENT
                h += SLIDE_INCREMENT
                w = 0

            # Save slice to tmp/slices folder
            scan = numpy_image[s, :height, :width]
            Image.fromarray(scan * 255).convert("L").save(os.path.join(slice_filepath, str(s) + ".tiff"))
            im = Image.open(os.path.join(slice_filepath, str(s) + ".tiff"))
 
            if os.path.isfile(os.path.join(slice_filepath, str(s) + ".jpg")):
                print("A jpeg file already exists for")
            else:
                outfile = os.path.join(slice_filepath, str(s) + ".jpg")
                try:
                    im.save(outfile, "JPEG", quality=100)
                except Exception as e:
                    print(e)

            s += 1
            h = 0

    print(test)


# Main
# Code to make temp directories to save stuff in
def setupDirectories(text):
    directory = text #"C:\\Users\\Jonathan Lehto\\Documents\\GitHub\\LungCancerDetection\\python\\example_subset_raw"
    cwd = os.getcwd()
    tmp_path = cwd + "\\tmp"
    slice_path = tmp_path + "\\slices"
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    if not os.path.exists(slice_path):
        os.mkdir(slice_path)

    # Run through all patches on all scans within directory
    for file_name in os.listdir(directory):
        file = os.path.join(directory, file_name)
        if ".mhd" in file_name:
            get_patches(file, slice_path, tmp_path)
    return tmp_path