from utility.image.convert_to_numpy import convert_to_numpy
from utility._file.split_data import split_data

root_path = ""
split_index = 200

split_data(root_path, split_index)
convert_to_numpy(root_path)
