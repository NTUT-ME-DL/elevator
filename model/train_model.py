from model import resnet
import os
import pandas as pd
import numpy as np
from keras.utils import np_utils

def getCurrentMemoryUsage():
    # Memory usage in kB
    try:
        with open('/proc/self/status') as f:
            memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]

        return int(memusage.strip()) / 1024
    except:
        return "The function that get Current memory usage of the current process only support on Linux"


def get_label(label_info, write_count):
    label_info = label_info[label_info["write_count"] == write_count]
    labels_count = (label_info["end_image_count"] - label_info["start_image_count"]).values
    
    label = []
    for floor, label_count in zip(range(len(labels_count)), labels_count):
        label += [floor] * label_count

    return np_utils.to_categorical(label)


# 2 min
def get_model():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

    image_width, image_height, image_channel = 96, 100, 3
    model = resnet.ResnetBuilder.build_resnet_34((image_channel, image_width, image_height), 12)

    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['categorical_accuracy']
    )
    
    return model


root_path = "/media/darkfanxing/Transcend/0527/training/"

model = get_model()
is_save_model_architecture = False
save_model_path = "/media/darkfanxing/Transcend/0527/model/resnet_3"

files_name = [name for name in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, name))]
data_files = files_name[:-1]
label_info = pd.read_csv(root_path + files_name[-1])

for index, data_file in zip(range(len(data_files)), data_files): 
    data = np.load(root_path + data_file)
    label = get_label(label_info, index)
    model.fit(x=data, y=label, epochs=2, batch_size=20, verbose=1)

if is_save_model_architecture:
    with open("{}.json".format(save_model_path), "w") as f:
        f.write(model.to_json())

model.save_weights("{}.h5".format(save_model_path))

root_path = "/media/darkfanxing/Transcend/0527/test/"
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