from PIL import Image
import numpy as np
from image_processing import image_processing
import sys, os

top_folder_path = os.getcwd()
data_processing_utility_folder_path = top_folder_path.split("course_title")[0] + "course_title\\data_processing\\utility"
sys.path.append(data_processing_utility_folder_path)

from normalize_image import normalize_image
from _file.get_label_count import get_label_count

def convert_to_numpy(root_path):
    data_types = ['training', 'test']
    for data_type in data_types:
        floor_path = "{}{}/".format(root_path, data_type)
        
        store = None
        label_count = get_label_count(floor_path)
        for key, image_count in label_count.items():
            image_data = np.zeros((1, 100, 100))
            
            for count in range(image_count):
                image = cv2.imread("./0525/training/{}f/{}.png".format(key, count))
                image = image_processing(image)
                image = normalize_image(image)

                image_data = np.concatenate((image_data, image), axis=0)
            
            image_data = image_data[1:, :, :]

            if store is None:
                store = image_data
            else:
                store = np.vstack((store, image_data))
                
        np.save("{}size_100_{}.npy".format(floor_path, data_type), store)