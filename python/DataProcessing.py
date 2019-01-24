import SimpleITK
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt
import scipy.ndimage
import math

# Constants
INITIAL_PATCH_WIDTH = 92        # This is the width in pixels need to allow for 64 pixel patch after 45 deg rotation
FINAL_PATCH_WIDTH = 64          # This is the number of pixels wanted in the final patch
ROTATION_DEGREE = 30            # Sets the rotation increment for data augmentation


def load_itk_image(filename):
    itk_image = SimpleITK.ReadImage(filename)

    numpy_image = SimpleITK.GetArrayFromImage(itk_image)
    numpy_origin = np.array(list(reversed(itk_image.GetOrigin())))
    numpy_spacing = np.array(list(reversed(itk_image.GetSpacing())))

    return numpy_image, numpy_origin, numpy_spacing


def read_csv(filename):
    lines = []
    with open(filename, "rt") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            lines.append(line)
    return lines


def world_2_voxel(world_coord, origin, spacing):
    stretched_voxel_coord = np.absolute(world_coord - origin)
    voxel_coord = stretched_voxel_coord / spacing
    return voxel_coord


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


def show_full_image(filepath, candidate_list):
    numpy_image, numpy_origin, numpy_spacing = load_itk_image(filepath)

    pat_id = path_to_id(filepath)
    for cand in candidate_list:
        if cand[0] == pat_id:
            # Get Candidates
            world_coord = np.asarray([float(cand[3]), float(cand[2]), float(cand[1])])
            voxel_coord = world_2_voxel(world_coord, numpy_origin, numpy_spacing)

            # get the whole image, from 0 to the size in both x and y plain
            patch = numpy_image[int(voxel_coord[0]), :numpy_image.shape[1], :numpy_image.shape[2]]
            patch = normalize_planes(patch)
            output_dir = "fullImages"
            plt.imshow(patch, cmap="gray")
            plt.show()
            pat_id = path_to_id(filepath)
            Image.fromarray(patch * 255).convert("L").save(os.path.join(output_dir, pat_id + ".tiff"))


def rotate_crop(image, initial_size, rotation, final_size):
    # This can be set to resample as NEAREST, BILINEAR, or BICUBIC
    r_patch = image.rotate(rotation, resample=Image.BICUBIC)
    center = initial_size / 2
    half_w = final_size / 2
    c_patch = r_patch.crop((math.floor(center - half_w), math.floor(center - half_w),
                           math.floor(center + half_w), math.floor(center + half_w)))
    return c_patch


# Show the plot of the image
def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.show()


# Given the file path to the image, search the CSV for any nodules that are related to that scan and display them.
def show_nodule(filepath, candidate_list):
    numpy_image, numpy_origin, numpy_spacing = load_itk_image(filepath)

    pat_id = path_to_id(filepath)
    for cand in candidate_list:
        if cand[0] == pat_id:
            # Get Candidates in Z, Y, X coordinates
            world_coord = np.asarray([float(cand[3]), float(cand[2]), float(cand[1])])
            voxel_coord = world_2_voxel(world_coord, numpy_origin, numpy_spacing)
            voxel_width = INITIAL_PATCH_WIDTH

            coord_start = [0, 0, 0]
            coord_end = [0, 0, 0]
            img_slice = int(voxel_coord[0])
            coord_start[1] = max(0, int(voxel_coord[1] - voxel_width / 2))
            coord_end[1] = min(int(voxel_coord[1] + voxel_width / 2), numpy_image.shape[1])
            coord_start[2] = max(0, int(voxel_coord[2] - voxel_width / 2))
            coord_end[2] = min(int(voxel_coord[2] + voxel_width / 2), numpy_image.shape[2])

            patch = numpy_image[img_slice, coord_start[1]:coord_end[1], coord_start[2]:coord_end[2]]
            patch = normalize_planes(patch)

            if "cand" in filepath:
                out_dir = "patches/test/"
                x = str(world_coord[2])
                y = str(world_coord[1])

                # Save image to folder for machine learning algorithm
                patch = Image.fromarray(patch * 255).convert("L")

                # Do data set augmentation on nodules that are positive
                if int(cand[4]):
                    # Rotations
                    for rot in range(0, 360, ROTATION_DEGREE):
                        r_path = os.path.join(out_dir, str(cand[4]) + "_r" + str(rot) + "_X" + x + "_Y" + y + ".tiff")
                        f_path = os.path.join(out_dir, str(cand[4]) + "_f" + str(rot) + "_X" + x + "_Y" + y + ".tiff")

                        # Rotate and flip patches and then save to path
                        r_patch = rotate_crop(patch, INITIAL_PATCH_WIDTH, rot, FINAL_PATCH_WIDTH)    # Rotate, then
                        f_patch = patch.transpose(Image.FLIP_LEFT_RIGHT)                             # Flip
                        r_patch.save(r_path)
                        f_patch.save(f_path)
                else:
                    image_path = os.path.join(out_dir, str(cand[4]) + "_r0_X" + x + "_Y" + y + ".tiff")
                    patch = rotate_crop(patch, INITIAL_PATCH_WIDTH, 0, FINAL_PATCH_WIDTH)  # Must crop from 92 pixels
                    patch.save(image_path)

            else:
                out_dir = "patches/test/"
                patch = Image.fromarray(patch * 255).convert("L")

                # Rotations
                for rot in range(0, 360, ROTATION_DEGREE):
                    r_path = os.path.join(out_dir, "test_patch_" + str(world_coord[2]) + "_R" + str(rot) + ".tiff")
                    r_patch = rotate_crop(patch, INITIAL_PATCH_WIDTH, rot, FINAL_PATCH_WIDTH)
                    r_patch.save(r_path)


# Print out all nodules that correspond to patient
def print_nodules(filepath, candidates_list):
    found = False
    pat_id = path_to_id(filepath)
    for cand in candidates_list:
        if cand[0] == pat_id:
            if not found:
                print("Patient found: " + pat_id)
            print("\t\tLocation is (X, Y, Z):", cand[1], ",", cand[2], ",", cand[3])
            found = True


def path_to_id(filepath):
    last_period = filepath.rfind(".")
    last_slash = filepath.rfind("\\") + 1
    pat_id = filepath[last_slash:last_period]
    return pat_id


cand_path = "E:\\Fall 2018\\EE4901\\Data\\annotations.csv"
directory = "E:\\Fall 2018\\EE4901\\CancerDetectionProgram\\Data\\subset_ex"
ex_dir = "./Data/subset0"

candidates = read_csv(cand_path)

# Print out the nodules for each file in the directory
for file_name in os.listdir(directory):
    file = os.path.join(directory, file_name)
    if ".mhd" in file_name:
        show_nodule(file, candidates)
        print_nodules(file, candidates)
        # showFullImage(file, candidates)
