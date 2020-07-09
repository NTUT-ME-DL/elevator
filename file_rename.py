import os

data_types = ['training', 'test']
for data_type in data_types:
  for floor in range(12):
      root_path = "/media/darkfanxing/Transcend/data/{}/{}f/".format(data_type, floor)
      f = os.listdir(root_path)

      count = 0
      for _ in f:
        old_name = f[count]
        
        # set the new name
        new_name = "{}.png".format(count)
      
        os.rename(root_path + old_name, root_path + new_name)
        print(old_name, "======>", new_name)

        count += 1