import pandas as pd
from keras.models import model_from_json
import numpy as np
import os
from keras.utils import np_utils

def get_label(label_info, write_count):
    label_info = label_info[label_info["write_count"] == write_count]
    labels_count = (label_info["end_image_count"] - label_info["start_image_count"]).values
    
    label = []
    for floor, label_count in zip(range(len(labels_count)), labels_count):
        label += [floor] * label_count

    return np_utils.to_categorical(label)


def get_model(architecture_file_path, model_weights_file_path):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
    
    with open("{}.json".format(architecture_file_path), "r") as json_file:
        model = model_from_json(json_file.read())

    model.load_weights("{}.h5".format(model_weights_file_path))
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["categorical_accuracy"]
    )
    
    return model


def getCurrentMemoryUsage():
    # Memory usage in kB
    try:
        with open('/proc/self/status') as f:
            memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]

        return int(memusage.strip()) / 1024
    except:
        return "The function that get Current memory usage of the current process only support on Linux"


root_path = "/media/darkfanxing/Transcend/0527/test/"

model = get_model("/media/darkfanxing/Transcend/0527/model/resnet", "/media/darkfanxing/Transcend/0527/model/resnet_2")

files_name = [name for name in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, name))]
data_files = files_name[:-1]
label_info = pd.read_csv(root_path + files_name[-1])

for index, data_file in zip(range(len(data_files)), data_files): 
    data = np.load(root_path + data_file)
    label = get_label(label_info, index)
    print(data.shape)
    print(label.shape)
    loss, accuary = model.evaluate(data, label)
    print("test loss: {}".format(loss))
    print("test accuary: {}".format(accuary))