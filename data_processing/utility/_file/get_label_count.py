import os

def get_label_count(root_path):
    label_count = {}
    for floor in range(11):
        path = "{}{}f/".format(root_path, floor)
        file_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        label_count[str(floor)] = file_count
    
    return label_count