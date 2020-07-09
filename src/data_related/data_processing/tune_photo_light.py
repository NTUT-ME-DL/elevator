import os
import cv2
import numpy as np

is_minus = True

data_types = ["training", "test"]
for data_type in data_types:
  for change_percentage in range(0.1, 0.4 + 0.1, 0.1):
    for floor in range(11):
      root_path = "/media/darkfanxing/Transcend/0527/{}/{}f/".format(data_type, floor)
      files = os.listdir(root_path)
      
      image_data = np.zeros((1, 96, 128, 3))
      for file_name in files:
        image = cv2.imread(root_path + file_name)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        if is_minus:
          image[..., 2] -= int(255 * change_percentage)
          image[..., 2] = np.where(image[..., 2] >= 256 - int(255 * change_percentage), 0, image[..., 2])
        else:
          image[..., 2] += int(255 * change_percentage)
          image[..., 2] = np.where(image[..., 2] < int(255 * change_percentage), 255, image[..., 2])

        image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
        image_data = np.concatenate((image_data, image), axis=0)

      image_data = image_data[1:, :, :]
      store = image_data if store is None else np.vstack((store, image_data))
      with open("{}np_file_description.csv".format(data_type_path), "a", newline="") as csv_file:
          writer = csv.writer(csv_file)
          writer.writerow([
              floor,
              write_count,
              image_count_per_file * write_count,
              end_image_count
          ])

    np.save("{}data_{}.npy".format(data_type_path, write_count), store)
    write_count += 1