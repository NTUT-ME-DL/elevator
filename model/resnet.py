from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import np_utils
import resnet

def show_image(image):
    plt.gcf().set_size_inches(2, 2) # setting image of width and height
    plt.imshow(image, cmap='binary') # drawing a picture
    plt.show() # print image


def show_train_model(train_model, train, validation):
    plt.plot(train_model.history[train])
    plt.plot(train_model.history[validation])
    plt.title('Train model')
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()


def save_image():
    count = 0

    while (count < 10030):
        image = Image.open("D:/test/{}.png".format(count)) # mode = RGB, size = 640 * 480
        image = image.convert('L').resize([100, 100]) # mode = L, size = 100 * 100, L is grayscale that 0 ~ 255 pixel
        
        image = np.array(image) 
        image = 255 - image # invert grayscale image
        image = image.reshape(1, 100, 100).astype('float32')
        
        if(count == 0):
            image_numpy_arrays = image
        else:
            image_numpy_arrays = np.concatenate((image_numpy_arrays, image), axis=0)
        
        count += 1

    np.save("D:/test/image_numpy_arrays.npy", image_numpy_arrays)


def image_array_and_labels():
    image_numpy_array = np.load("D:/test/image_numpy_arrays.npy") # the size of matrix is (image_count, 100, 100)
    image_numpy_array = np.expand_dims(image_numpy_array, axis=3) # becomes a four dimensional space, so the siez of matrix is (image_count, 100, 100, 1)

    images_count = [995, 1107, 994, 960, 997, 992, 998, 989, 995, 1002]
    labels = []

    for index, value in enumerate(images_count):
        labels += [index] * value

    labels = np_utils.to_categorical(labels) # one-hot encoding, if label = 0, it will convert to [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    np.savetxt("D:/test/image_one_hot_encoding_label.txt")
    return image_numpy_array, labels


model = resnet.ResnetBuilder.build_resnet_34(input_shape=(1, 100, 100), num_outputs=10)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

image_array, labels = image_array_and_labels()

train_model = model.fit(x=image_array, y=labels, validation_split=0,
                            epochs=50, batch_size=50, verbose=2)

show_train_model(train_model, 'acc','val_acc')
show_train_model(train_model, 'loss','val_loss')

with open("./resnet_34_model.json", "w") as json_file:
    json_file.write(model.to_json())

# serialize weights to HDF5
model.save_weights("./resnet_34_model.h5")
print(model.summary())