import serial
import sys
import cv2
import numpy as np
import json
from keras.utils import np_utils
from keras.models import model_from_json
from time import sleep
from PIL import Image
import os, sys
import keyboard

top_folder_path = os.getcwd().split("course_title")[0]
data_processing_utility_folder_path = top_folder_path + "course_title\\data_processing\\utility"
model_utility_path = top_folder_path + "course_title\\model\\utility"
sys.path.append([data_processing_utility_folder_path, model_utility_path])

from image_processing import image_processing
from load_model import load_model

architecture_file_path = "D:/model/size_100_resnet_34"
model_weights_file_path = "D:/model_100_resnet_34_0224_5"
model = load_model(architecture_file_path, model_weights_file_path)

camera = cv2.VideoCapture(1)
com_port = "COM3"
baud_rates = 9600
serial = serial.Serial(com_port, baud_rates)

def sent_data(data):
  serial.write(data.encode())
  while serial.in_waiting:
    mcu_feedback = serial.readline().decode()  # 接收回應訊息並解碼
    print('控制板回應：', mcu_feedback)

def detect_key():
  for floor in range(10):
    if keyboard.is_pressed(str(floor)):
      sent_data("close-" + str(floor))

def get_realtime_predict():
  _, image = camera.read()
  cv2.imshow("camera", image)
  
  image = image_processing(image)
  cv2.imshow("image_process", image)

  image = image / 255.
  image -= 0.5
  image *= 2.
  
  image = np.expand_dims(image, axis=0)
  image = np.expand_dims(image, axis=3)
    
  predict = model.predict(image)
  predict = np.argmax(predict)
  return predict

while True:
  try:
    predict = get_realtime_predict()
    print()
    floor = str(predict) + "\n"
    if floor != "10\n":
      sent_data(floor)
    
    detect_key()
    serial.close()
    serial.open()

  except KeyboardInterrupt:
      serial.close()
      print('serial close！')