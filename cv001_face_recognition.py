import cv2
from collections import deque
import time
import numpy

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# face_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
camera = cv2.VideoCapture(0)  # 打开摄像头
time.sleep(2)  # 等待两秒
# 遍历每一帧，检测红色瓶盖
while True:
    (ret, frame) = camera.read()   # 读取帧
    if not ret:  # 判断是否成功打开摄像头
        print('No Camera')
        break
    # frame = imutils.resize(frame, width=600)
    # 转到HSV空间
    dst = cv2.resize(frame, (500, 500), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('YZN', dst)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# cv2.waitKey(0)
cv2.destroyAllWindows()
