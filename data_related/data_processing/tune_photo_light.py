import os
import cv2

data_types = ['training', 'test']
for data_type in data_types:
  for floor in range(11):
      root_path = "F:/0408_0414/{}/{}f/".format(data_type, floor)
      files = os.listdir(root_path)

      for _file in files:
        img = cv2.imread("file_name", )
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 設定欲檢哨的飽和度百分比
        change_percentage = 0.2

        img_hsv[..., 1] -= 255 * change_percentage
        img_hsv[img_hsv[..., 1] < 0] = 0