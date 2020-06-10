import os
import cv2
import numpy as np

def sobel(image):
    abs_x = cv2.convertScaleAbs(cv2.Sobel(image, cv2.CV_16S, 1, 0))
    abs_y = cv2.convertScaleAbs(cv2.Sobel(image, cv2.CV_16S, 0, 1))
    image = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)

    return image

def remove_small_contours(image, specified_area):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < specified_area:
            image = cv2.drawContours(image,[contours[i]], 0, 0, -1)
    
    return image

def adjust_saturation_and_value(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    image[..., 1] -= 35
    image[image[..., 1] >= 220] = 0
    image[..., 2] -= 130
    image[image[..., 2] >= 105] = 0
    image[image[..., 1] <= 1] = 255

    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    return image

def image_processing(image):
    image = adjust_saturation_and_value(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.medianBlur(image, 5)
    image = sobel(image)
    image = remove_small_contours(image, 1900)
    cv2.imshow("image_processing", image)
    image = cv2.resize(image, (100, 100), cv2.INTER_NEAREST)
    return image