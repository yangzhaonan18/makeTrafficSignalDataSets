# coding:utf-8
# name  : cv2.HoughCircles

import cv2
import numpy as np

planets = cv2.imread('C:\\Users\\young\\Desktop\\just\\2000\\998.png')
gray_img = cv2.cvtColor(planets, cv2.COLOR_BGR2GRAY)
# 模糊
img = cv2.medianBlur(gray_img, 3)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cimg = cv2.pyrMeanShiftFiltering(cimg, 10, 100)
'''
cv2.HoughCircles(image, method, dp, minDist, circles, param1, param2, minRadius, maxRadius)
method:用于检测的方法，现在只有HOUGH_GRADIENT
dp:累加器分辨率：dp=1跟原图有同样的分辨率，dp=2分辨率是原图的一般
minDist：圆心到圆的最短距离
param1:First method-specific parameter。在HOUGH_GRADIENT里面，是Canny边缘检测较大的那个参数
param2:累加器在检测时候圆心的阀值。约小约容易检测到假圆
'''
cv2.imshow("Blur", img)
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 60, param1=130, param2=30, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    # 圆
    cv2.circle(planets, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # 中心点
    cv2.circle(planets, (i[0], i[1]), 2, (0, 0, 255), 3)
cv2.imwrite("planets_circles.jpg", planets)
cv2.imshow("HoughCirlces", planets)
cv2.waitKey(0)
