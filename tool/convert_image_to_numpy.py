from PIL import Image
import numpy as np
import os

image_size = 100

data_types = ['training', 'test']
for data_type in data_types:
  root_path = "F:/0408_0414/{}/".format(data_type)
  
  label_count = {}
  for i in range(10):
      path = "{}{}f/".format(root_path, i)
      file_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
      label_count[str(i)] = file_count

  store = None
  for key, image_count in label_count.items():
      count = 0
      img_data = np.zeros((1, image_size, image_size)) 
      while (count < image_count):
          img = np.array(Image.open("{}{}f/{}.png".format(root_path, key, count)).convert("L").resize([image_size, image_size], Image.ANTIALIAS))
          
          img = img / 255.
          img -= 0.5
          img *= 2.
          img = np.expand_dims(img, axis=0)
          
          img_data = np.concatenate((img_data, img), axis=0)
      
          print(count)
          count += 1
      
      img_data = img_data[1:, :, :]

      if store is None:
          store = img_data
      else:
          store = np.vstack((store, img_data))
      
      print(store.shape)

  np.save("{}size_{}_{}_total.npy".format(root_path, image_size, data_type), store)