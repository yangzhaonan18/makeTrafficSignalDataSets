# -*- coding:utf-8 -*-
# 遍历文件夹下的图片，提取红黄蓝三种颜色下的区域
import os
import cv2
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import random


def cutout(img_path, save_path):
    mybuffer = 64
    pts = deque(maxlen=mybuffer)


    # 设定红色阈值，HSV空间
    # redLower = np.array([160, 100, 100])
    # redUpper = np.array([180, 255, 255])

    # 红色的阈值 标准H：0-10，156-180 S:43:255 V:46:255
    redLower01 = np.array([0, 80, 46])
    redUpper01 = np.array([15, 255, 255])
    redLower02 = np.array([160, 80, 46])
    redUpper02 = np.array([179, 255, 255])

    # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowLower = np.array([16, 80, 46])
    yellowUpper = np.array([34, 255, 255])

    # # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenLower = np.array([35, 80, 46])
    greenUpper = np.array([120, 255, 255])

    frame = cv2.imread(img_path)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜
    r1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 红色的两个区域
    r2_mask = cv2.inRange(hsv, redLower02, redUpper02)
    y_mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    g_mask = cv2.inRange(hsv, greenLower, greenUpper)

    mask = r1_mask + r2_mask + y_mask + g_mask

    mask = cv2.erode(mask, None, iterations=1)  # 腐蚀操作
    mask = cv2.dilate(mask, None, iterations=1)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    BlueThings = cv2.bitwise_and(frame, frame, mask=mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # 轮廓检测
    # 初始化瓶盖圆形轮廓质心



    center = None
    # 如果存在轮廓
    if len(cnts) > 0:
        # 找到面积最大的轮廓
        c = max(cnts, key=cv2.contourArea)
        # 确定面积最大的轮廓的外接圆

        ((x, y), radius) = cv2.minEnclosingCircle(c)
        print(((x, y), radius))
        # 计算轮廓的矩
        M = cv2.moments(c)
        # 计算质心
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print("center:", center)
        # 只有当半径大于10时，才执行画图
        if radius > 2:
            cv2.circle(BlueThings, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # 画圆
            cv2.circle(BlueThings, center, 1, (255, 255, 255), -1)   # 画点
            cv2.circle(BlueThings, (5, 5), 5, (255, 0, 0), 3)

            # 把质心添加到pts中，并且是添加到列表左侧
            pts.appendleft(center)

        dst = cv2.GaussianBlur(BlueThings, (5, 5), 0)
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imshow("binary image", binary)
        cv2.imwrite(save_path, BlueThings)  # 保存修改像素点后的图片

        gray = cv2.cvtColor(BlueThings, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(BlueThings, contours, -1, (0, 255, 255), 3)
        # cv2.imshow("img", BlueThings)
        # cv2.waitKey(1000)





if __name__ == "__main__":

    work_dir = "C:\\Users\\young\\Desktop\\just"
    # img_dir = "2001"
    # save_dir = "2001-after"
    # img_dir = "2002"
    # save_dir = "2002-after"
    img_dir = "2003"
    save_dir = "2003-after"

    img_dir = os.path.join(work_dir, img_dir)
    save_dir = os.path.join(work_dir, save_dir)
    img_list = os.listdir(img_dir)
    for img in img_list:
        img_path = os.path.join(img_dir, img)
        save_name = os.path.splitext(img)[0] + ".png"
        save_path = os.path.join(save_dir, save_name)
        # 处理每一张图片并保存
        cutout(img_path, save_path)

    print("Finish")
