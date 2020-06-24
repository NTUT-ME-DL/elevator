import cv2
import time
import os
import time

def get_file_count(root_path):
  file_count = len([name for name in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, name))])
  return file_count

def write_image(root_path, count):
  img_path = "{}{}.png".format(root_path, count)
  cv2.imwrite(img_path, frame)

video_capture = cv2.VideoCapture(0)

floor = input("floor:")
is_automatic = True if input("Do you want to automatic capture? (y or n) ") == "y" else False
root_path = "F:/0408_0414/test/{}f/".format(floor)

count = get_file_count(root_path)
if is_automatic:
  while (1):
    ret, frame = video_capture.read()
    cv2.imshow("Video", frame)

    cv2.waitKey(1)
    write_image(root_path, count)
    
    print(count)

    count += 1
    time.sleep(0.5)

else:
  while (1):
    ret, frame = video_capture.read()
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('\\'):
      write_image(root_path, count)
      
      print(count)
      count += 1

video_capture.release()
cv2.destroyAllWindows()