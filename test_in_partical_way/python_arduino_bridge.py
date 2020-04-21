import serial
import sys
import cv2
import numpy as np
import json
from keras.utils import np_utils
from keras.models import model_from_json
from time import sleep
from PIL import Image
import os

# load model
architecture_file_path = "D:/model/size_100_resnet_34"
model_weights_file_path = "D:/model_100_resnet_34_0224_5"

with open("{}.json".format(architecture_file_path), "r") as json_file:
  model = model_from_json(json_file.read())

model.load_weights("{}.h5".format(model_weights_file_path))
model.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=["categorical_accuracy"])

camara = cv2.VideoCapture(1)

com_port = "COM3"
baud_rates = 9600
serial = serial.Serial(com_port, baud_rates)

while True:
  count = 0
  photo_list = np.zeros((1, 100, 100, 1), dtype="float32")

  ret, frame = camara.read()
  cv2.imshow("img", frame)
  cv2.imwrite("photo/0.png", frame)
  
  cv2.waitKey(1)
  sleep(1)
        
  image = np.array(Image.open("photo/0.png").convert("L").resize([100, 100], Image.ANTIALIAS))
    
  image = image / 255.
  image -= 0.5
  image *= 2.
    
  image = np.expand_dims(image, axis=0)
  image = np.expand_dims(image, axis=3)
    
  predict = model.predict(image)
  predict = np.argmax(predict)
  print(predict)
  
  try:
    floor = str(predict) + "\n"
    if floor != "10\n":
      serial.write(floor.encode())
      while serial.in_waiting:
          mcu_feedback = serial.readline().decode()  # 接收回應訊息並解碼
          print('控制板回應：', mcu_feedback)

  except KeyboardInterrupt:
      serial.close()
      print('serial close！')