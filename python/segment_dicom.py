import sys
import os
import numpy
import pandas as pd
import pydicom
import scipy.ndimage
import SimpleITK as sitk
import matplotlib.pyplot as plt
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# This code is used to do all of the preprocessing of extracting patches for the machine learning algorithm
#	to train on. This is not used in the final app, but is a good resource to extract patches needed.
#	All normalizing algorithms are the same as the lung_to_patches.py and so the patches are treated the same.

# Load a scan and infer the pixel size in the Z direction, which is the slice_thickness
def load_scan(path):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    try:
        slice_thickness = numpy.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = numpy.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices


# Transform the images to represent HU, so that it corresponds to different parts of the body correctly
def get_pixels_hu(slices):
    image = numpy.stack([s.pixel_array for s in slices])

    # Convert to int16, should be possible as values should always be less than 32k
    image = image.astype(numpy.int16)

    # Set outside of scan pixels to 0, air is approximately 0
    image[image == -2000] = 0

    # Convert to Hounsfield units (HU)
    for slice_number in range(len(slices)):

        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope

        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(numpy.float64)
            image[slice_number] = image[slice_number].astype(numpy.int16)

        image[slice_number] += numpy.int16(intercept)

    return numpy.array(image, dtype=numpy.int16)


# Convert images to gave the same pixel spacing. This will help when comparing images from different machines
def resample(image, scan, new_spacing=[1, 1, 1]):
    # Determine current pixel spacing
    spacing = numpy.array([scan[0].SliceThickness, scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]], dtype=numpy.float32)

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = numpy.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')

    return image, new_spacing


# 3D plots of images
def plot_3d(image, threshold=-300):

    # Position the scan upright so head of patient would be at the top facing camera
    p = image.transpose(2, 1, 0)

    verts, faces = measure.marching_cubes_classic(p, threshold)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: verts[faces] to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.70)
    face_color = [0.45, 0.45, 0.45, 0.75]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    # Do this to be able to see 3d plot. Otherwise you get a single line.
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.show()


# Lung Segmentation Steps
# 1. Threshold the image to get correct tissue (-320)
# 2. Do connected components, determine label of air around person, fill this with 1s in binary image
# 3. Optionally: For every axial slice in the scan, determine the largest solid connected component
#       (the body+air around the person), and set others to 0. This fills the structures in the lungs in the mask.
# 4. Keep only largest air pocket

def largest_label_volume(im, bg=-1):
    vals, counts = numpy.unique(im, return_counts=True)

    counts = counts[vals != bg]
    vals = vals[vals != bg]

    if len(counts) > 0:
        return vals[numpy.argmax(counts)]
    else:
        return None


def segment_lung_mask(image, fill_lung_structures=True):
    # Not really binary, but 1 and 2. 0 is treated as background, which we dont want
    binary_image = numpy.array(image > -320, dtype=numpy.int8) + 1
    labels = measure.label(binary_image)

    # Pick the pixel in the very corner to determine which label is air.
    #   Improvement: Pick multiple background labels from around the patient
    #   More resistant to "trays" on which the patient lays cutting the air
    #   around the person in half

    background_label = labels[0, 0, 0]

    # Fill the air around the person
    binary_image[background_label == labels] = 2

    # Method of filling the lung structures (that is superior to morphological closing)
    if fill_lung_structures:
        # For every slice we determine the largest solid structure
        for i, axial_slice in enumerate(binary_image):
            axial_slice = axial_slice - 1
            labeling = measure.label(axial_slice)
            l_max = largest_label_volume(labeling, bg=0)

            if l_max is not None:
                binary_image[i][labeling != l_max] = 1

    binary_image -= 1  # Make the image actual binary
    binary_image = 1 - binary_image  # Invert it, lungs are now 1

    # Remove other air pockets inside body
    labels = measure.label(binary_image, background=0)
    l_max = largest_label_volume(labels, bg=0)
    if l_max is not None:                               # There are air pockets
        binary_image[labels != l_max] = 0

    return binary_image


def show_dcm_info(dataset):
    print("Filename: ", file_path)
    print("Storage Type: ", dataset.SOPClassUID)
    print()

    pat_name = dataset.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    print("Patients Name: ", display_name)
    print("Patient id..........:", dataset.PatientID)
    print("Modality............:", dataset.Modality)

# MAIN
# "C:\\Users\\Jonathan Lehto\\Documents\\GitHub\\LungCancerDetection\\python\\dicom\\"

def evaluate(path):
    INPUT_FOLDER = path + "\\"
    patients = os.listdir(INPUT_FOLDER)
    patients.sort()

    file_path = INPUT_FOLDER + patients[0]
    disp_images = True
    # Show histogram of HU values present in image
    first_patient = load_scan(file_path)
    # Set up dataset with all patient information
    i = 1
    num_to_plot = 5
    for file_name in os.listdir(file_path):
        file = os.path.join(file_path, file_name)
        dataset = pydicom.dcmread(file)

        if i >= num_to_plot:
            break
        i += 1

    first_patient_pixels = get_pixels_hu(first_patient)
    plt.hist(first_patient_pixels.flatten(), bins=80, color='c')
    plt.xlabel("Hounsfield Units (HU)")
    plt.ylabel("Frequency")
    if not os.path.exists(path + "\\tempdata"):
        os.makedirs(path + "\\tempdata")

    plt.savefig(path + "\\tempdata\\plot.png")
    return path + "\\tempdata\\plot.png"
