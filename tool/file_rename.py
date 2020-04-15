import os

is_add_file_name = input("Do you want to add additional file name? (y or n)")
additional_file_name = input("Please input the additional file name:") if is_add_file_name == "y" else ""

data_types = ['training', 'test']
for data_type in data_types:
  for floor in range(11):
      root_path = "F:/0408_0414/{}/{}f/".format(data_type, floor)
      f = os.listdir(root_path)

      count = 0
      for _ in f:
        old_name = f[count]
        
        # set the new name
        new_name = "{}.png".format(count)
      
        os.rename(root_path + old_name, root_path + new_name)
        print(old_name, "======>", new_name)

        count += 1