import serial
import sys
import cv2
import numpy as np
import json
from keras.utils import np_utils
from time import sleep
from PIL import Image
import os, sys
import keyboard
import datetime

from image_processing import image_processing
from load_model import load_model

architecture_file_path = "D:/course_title/model/model_100_resnet_34_adjust_0527_epoch5_batchsize20"
model_weights_file_path = "D:/course_title/model/model_100_resnet_34_adjust_0527_epoch5_batchsize20"
model = load_model(architecture_file_path, model_weights_file_path)

camera = cv2.VideoCapture(0)
com_port = "COM8"
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
      sent_data("close-" + str(floor) + "\n")
  
  if keyboard.is_pressed('r'):
    sent_data("reset\n")

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

prior_floor = "\n"
count = 0
while True:
  try:
    sleep(0.3)
    start_time = datetime.datetime.now().microsecond / 10 ** 6
    detect_key()
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

    predict = get_realtime_predict()
    
    if count == 0:
      sent_data("reset\n")
      count += 1
      continue

    floor = str(predict) + "\n"
    if floor == prior_floor:
      continue
    else:
      if floor != "10\n":
        sent_data(floor)
    
      if prior_floor == "0\n":
        sent_data("close-0\n")
      elif prior_floor == "9\n":
        sent_data("close-9\n")

      prior_floor = floor
  except KeyboardInterrupt:
    serial.close()
    print('serial close！')
    break