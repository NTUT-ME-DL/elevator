import os

def file_rename(root_path, additional_file_name):
  # is_add_file_name = input("Do you want to add additional file name? (y or n)")
  # additional_file_name = input("Please input the additional file name:") if is_add_file_name == "y" else ""

  data_types = ['training', 'test']
  for data_type in data_types:
    for floor in range(11):
        floor_path = "{}{}/{}f/".format(root_path, data_type, floor)
        file_names = os.listdir(floor_path)
        
        for count in range(len(file_names)):
          old_name = file_names[count]
          new_name = "{}{}.png".format(count, additional_file_name)
        
          os.rename(floor_path + old_name, floor_path + new_name)
          print(old_name, "======>", new_name)

if __name__ == "__main__":
  file_rename("F:/0408_0414/", "a")