import os
import cv2
import numpy as np

data_types = ['training', 'test']
for data_type in data_types:
  for floor in range(11):
      root_path = "C:/Users/AILab/Documents/elevator/data/0520/"

      folder_path = "{}{}/{}f/".format(root_path, data_type, floor)
      file_names = os.listdir(folder_path)

      for file_name in file_names:
          file_path = folder_path + file_name

          orig_image = cv2.imread(file_path)
          image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2HSV)

          image[..., 1] -= 35
          image[image[..., 1] >= 220] = 0

          image[..., 2] -= 130
          image[image[..., 2] >= 105] = 0

          image[..., 1] += 1
          image[image[..., 2] <= 1] = 255

          image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
          image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
          cv2.imwrite("{}adjust_{}/{}f/{}".format(root_path, data_type, floor, file_name), image)
          # cv2.imshow("123", np.vstack((image, orig_image)))

          # key = cv2.waitKey(0)
          # if key == 27:
          #   cv2.destoryAllWindows()
          #   break
