import shutil
import os
import random
from file_rename import file_rename

def split_data(root_path, split_index):
  for floor in range(11):
    original_root_path = "{}training/{}f".format(root_path, floor)
    target_root_path = "{}test/{}f".format(root_path, floor)

    file_names = [name for name in os.listdir(original_root_path) if os.path.isfile(os.path.join(original_root_path, name))]
    
    random_indices = [index for index in range(len(file_names))]
    random.shuffle(random_indices)
    
    for index in range(split_index):
      index = random_indices[index]
      file_name = file_names[index]
      
      original_path = "{}/{}".format(original_root_path, file_name)
      target_path = "{}/{}".format(target_root_path, file_name)
      shutil.move(original_path, target_path)

  file_rename(root_path, "_")
  file_rename(root_path, "")