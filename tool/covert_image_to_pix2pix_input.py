import numpy as np
import cv2
from PIL import Image
import os


data_types = ['training', 'test']
for data_type in data_types:
  root_path = "F:/0422/{}/".format(data_type)

  label_count = {}
  for i in range(11):
    path = "{}{}f/".format(root_path, i)
    file_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    label_count[str(i)] = file_count

  for key, image_count in label_count.items():
    for count in range(image_count):
      image = np.array(Image.open("{}{}f/{}.png".format(root_path, key, count)).resize([256, 256]))
      image = np.hstack((image, image))
      cv2.imwrite("{}pix2pix/{}f/{}.png".format(root_path, key, count), image)
      print("{}pix2pix/{}f/{}.png".format(root_path, key, count))