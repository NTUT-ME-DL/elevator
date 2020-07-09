import numpy as np
import cv2
import os
import csv

def get_label_count(root_path):
    label_count = {}
    for floor in range(12):
        path = "{}{}f/".format(root_path, floor)
        file_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        label_count[floor] = file_count

    return label_count


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (128, 96), cv2.INTER_NEAREST)
    image = np.expand_dims(image, axis=0)
    print(image_path)
    
    return image


def convert_to_numpy(root_path, image_count_per_file, is_minus=None, change_percentage=0):
    if is_minus is not None:
        image_type = "-" if is_minus else "+"
        image_type += str(change_percentage)
    else:
        image_type = str(change_percentage)
                        
    for data_type in ["training", "test"]:
        data_type_path = "{}{}/".format(root_path, data_type)

        label_count = get_label_count(data_type_path)

        write_count = 0
        for image_count in range(0, label_count[min(label_count, key=label_count.get)] + 1, 400):
            store = None
            for floor in range(12):
                image_data = np.zeros((1, 96, 128, 3))
                
                if label_count[floor] <= image_count + image_count_per_file:
                    end_image_count = label_count[floor] - image_count + image_count_per_file *  write_count
                else:
                    end_image_count = image_count + image_count_per_file

                for count in range(image_count_per_file * write_count, end_image_count, 1):
                    image_path = "{}{}f/{}.png".format(data_type_path, floor, count)
                    image = get_image(image_path)
                    
                    if is_minus is not None:
                        if is_minus:
                            image[..., 2] -= int(255 * change_percentage)
                            image[..., 2] = np.where(image[..., 2] >= 256 - int(255 * change_percentage), 0, image[..., 2])
                        else:
                            image[..., 2] += int(255 * change_percentage)
                            image[..., 2] = np.where(image[..., 2] < int(255 * change_percentage), 255, image[..., 2])
                        
                    
                    image_data = np.concatenate((image_data, image), axis=0)

                image_data = image_data[1:, :, :]
                store = image_data if store is None else np.vstack((store, image_data))
                with open("{}np_file_description.csv".format(data_type_path), "a", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                        
                    writer.writerow([
                        floor,
                        write_count,
                        image_count_per_file * write_count,
                        end_image_count,
                        image_type
                    ])

            np.save("{}data_{}_{}.npy".format(data_type_path, write_count, image_type), store)
            write_count += 1

if __name__ == "__main__":
    root_path = "/media/darkfanxing/Transcend/data/"
    additional_data = True
    image_count_per_file = 300
    
    for data_type in ["training", "test"]:
        with open("{}{}/np_file_description.csv".format(root_path, data_type), "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["floor", "write_count","start_image_count", "end_image_count", "type"])
    
    convert_to_numpy(root_path, image_count_per_file)
    for change_percentage in range(0.1, 0.4 + 0.1, 0.1):
        convert_to_numpy(root_path, image_count_per_file, is_minus=True, change_percentage=change_percentage)
        convert_to_numpy(root_path, image_count_per_file, is_minus=False, change_percentage=change_percentage)