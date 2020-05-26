import os
import cv2
import numpy as np

def salt(img, n):
    for _ in range(n):
        i = int(np.random.random() * img.shape[1])
        j = int(np.random.random() * img.shape[0])
        if img.ndim == 2:
            img[j,i] = 255
        elif img.ndim == 3:
            img[j,i,0]= 255
            img[j,i,1]= 255
            img[j,i,2]= 255
        return img

def image_processing(image):
    image[..., 1] -= 35
    image[image[..., 1] >= 220] = 0

    image[..., 2] -= 130
    image[image[..., 2] >= 105] = 0

    image[..., 1] += 1
    image[image[..., 2] <= 1] = 255

    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    image = cv2.medianBlur(salt(image, 500), 5)

    abs_x = cv2.convertScaleAbs(cv2.Sobel(image, cv2.CV_16S, 1, 0))
    abs_y = cv2.convertScaleAbs(cv2.Sobel(image, cv2.CV_16S, 0, 1))
    image = cv2.addWeighted(abs_x, 0.5, abs_y,0.5,0)

    contours, hierarch = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    print(len(contours))
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 3000:
            image = cv2.drawContours(image,[contours[i]], 0, 0, -1)
    
    return image