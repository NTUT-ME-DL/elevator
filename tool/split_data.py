import shutil
import os

split_index = 200

for floor in range(11):
  original_root_path = "F:/0408_0414/training/{}f".format(floor)
  target_root_path = "F:/0408_0414/test/{}f".format(floor)

  file_names = [name for name in os.listdir(original_root_path) if os.path.isfile(os.path.join(original_root_path, name))]
  for index in range(split_index):
    file_name = file_names[index]
    
    original_path = "{}/{}".format(original_root_path, file_name)
    target_path = "{}/{}".format(target_root_path, file_name)
    shutil.move(original_path, target_path)