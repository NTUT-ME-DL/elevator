import resnet
import os
import pandas as pd
import numpy as np
from keras.utils import np_utils

def get_label(label_info, write_count):
    label_info = label_info[label_info["write_count"] == write_count]
    labels_count = (label_info["end_image_count"] - label_info["start_image_count"]).values
    
    label = []
    for floor, label_count in zip(range(len(labels_count)), labels_count):
        label += [floor] * label_count

    return np_utils.to_categorical(label)


# exec time: 2 min
def get_model():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

    image_width, image_height, image_channel = 96, 100, 3
    model = resnet.ResnetBuilder.build_resnet_34((image_channel, image_width, image_height), 12)

    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['categorical_accuracy']
    )
    
    return model

def train_model(model, root_path, is_save_model_architecture, save_model_path):
    root_path += "training/"
    files_name = [name for name in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, name))]
    data_files = files_name[:-1]
    label_info = pd.read_csv(root_path + files_name[-1])

    for index, data_file in zip(range(len(data_files)), data_files): 
        data = np.load(root_path + data_file)
        label = get_label(label_info, index)
        model.fit(x=data, y=label, epochs=2, batch_size=20, verbose=1)

    return model

def test_model(model, root_path):
    root_path += "test/"
    files_name = [name for name in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, name))]
    data_files = files_name[:-1]
    label_info = pd.read_csv(root_path + files_name[-1])

    for index, data_file in zip(range(len(data_files)), data_files): 
        data = np.load(root_path + data_file)
        label = get_label(label_info, index)

        loss, accuary = model.evaluate(data, label)
        print("test loss: {}".format(loss))
        print("test accuary: {}".format(accuary))

if __name__ == "__main__":
    root_path = "/media/darkfanxing/Transcend/0527/"
    is_save_model_architecture = False
    save_model_path = "/media/darkfanxing/Transcend/0527/model/resnet_4"
    
    model = get_model()
    model = train_model(model, root_path, is_save_model_architecture, save_model_path)
    test_model(model, root_path)
    
    if is_save_model_architecture:
        with open("{}.json".format(save_model_path), "w") as f:
            f.write(model.to_json())

    model.save_weights("{}.h5".format(save_model_path))