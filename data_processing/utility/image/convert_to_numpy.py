from PIL import Image
import numpy as np
from image_processing import image_processing
import sys
import os
import cv2

top_folder_path = os.getcwd()
data_processing_utility_folder_path = top_folder_path.split("course_title")[0] + "course_title\\data_processing\\utility"
sys.path.append(data_processing_utility_folder_path)

from normalize_image import normalize_image
from _file.get_label_count import get_label_count

def reduce_brightness(image, value):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image[..., 2] -= value
    image[image[..., 2] > (255 - value)] = 0
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

    return image


def convert_to_numpy(root_path):
    data_types = ['training', 'test']
    for data_type in data_types:
        floor_path = "{}{}/".format(root_path, data_type)
        
        store = None
        label_count = get_label_count(floor_path)
        for key, image_count in label_count.items():
            image_data = np.zeros((1, 96, 128, 3))
            
            for count in range(image_count):
                image = cv2.imread("{}{}/{}f/{}.png".format(root_path, data_type, key, count))
                image = cv2.resize(image, (128, 96), cv2.INTER_NEAREST)

                image_data = np.concatenate((
                    image_data,
                    normalize_image(image),
                    normalize_image(reduce_brightness(image, 50)),
                    normalize_image(reduce_brightness(image, 100))
                ), axis=0)
            
            image_data = image_data[1:, :, :]
            print(key)

            if store is None:
                store = image_data
            else:
                store = np.vstack((store, image_data))
                
        np.save("{}size_100_{}.npy".format(floor_path, data_type), store)

convert_to_numpy("F:/0527/")