"""
Only for model case, else top 300 makes no sense for classes
"""

import os
from shutil import copy2
import pandas as pd

IMAGE_DIR = 'data/car-classifier-raw/'  # Directory images are stored in
STORAGE_DIR = 'data/'  # Directory to store split images

# Load prediction file created using notebook "prefilter.ipynb" in notebooks
df = pd.read_csv('data/filenames_with_car_flags_bw_added.csv', header=None, index_col=0, squeeze=True)

# List to store filenames of car images
car_images = []

# List to store filenames of non-car images
non_car_images = []

for file, car_flag in df.items():
    if car_flag:
        car_images.append(file)
    else:
        non_car_images.append(file)


print(len(car_images), len(non_car_images))


# Filter out classes with too few representatives (only for model)
def get_class_counts(files):
    """
    Get class label count from file paths
    """
    return pd.Series(['_'.join([file.split('_')[0], file.split('_')[1]]) for file in files]).value_counts()


to_filter = get_class_counts(car_images)[300:].keys()

files_filtered = [file for file in car_images if '_'.join([file.split('_')[0], file.split('_')[1]]) not in to_filter]

assert(len(car_images) - get_class_counts(car_images)[300:].sum() == len(files_filtered))

car_images = files_filtered

print(len(car_images))

storage_dir_ext = STORAGE_DIR

os.mkdir(storage_dir_ext + 'cars')
# os.mkdir(storage_dir_ext + 'non_cars')

for filename in car_images:
    copy2(IMAGE_DIR + filename, storage_dir_ext + 'cars')

# for filename in non_car_images:
#     copy2(IMAGE_DIR + filename, storage_dir_ext + 'non_cars')
