# -*- coding:utf-8 -*-

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random


def cutout(img_path, save_path):
    # 设定红色阈值，HSV空间
    # redLower = np.array([160, 100, 100])
    # redUpper = np.array([180, 255, 255])

    redLower01 = np.array([0, 80, 0])
    redUpper01 = np.array([15, 255, 255])

    redLower02 = np.array([160, 80, 0])
    redUpper02 = np.array([179, 255, 255])

    # x_min = float('inf')
    # y_min = float('inf')
    # x_max = 0
    # y_max = 0
    frame = cv2.imread(img_path)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜
    mask01 = cv2.inRange(hsv, redLower01, redUpper01)
    mask02 = cv2.inRange(hsv, redLower02, redUpper02)
    mask = mask01 + mask02

    # 腐蚀操作
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.erode(mask, None, iterations=2)
    # cv2.imshow('erode', frame)  # yzn
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, None, iterations=2)
    BlueThings = cv2.bitwise_and(frame, frame, mask=mask)
    # 轮廓检测
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 初始化瓶盖圆形轮廓质心
    print("BlueThings.shape:", BlueThings.shape)
    # print(cnts)
    # cv2.circle(BlueThings, (cnts[0][0], cnts[0][1]), 7, (0, 0, 255), 8)
    center = None

    cv2.imwrite(save_path, BlueThings)  # 保存修改像素点后的图片


if __name__ == "__main__":

    work_dir = "C:\\Users\\young\\Desktop\\just"
    img_dir = "2001"
    save_dir = "2001-after"
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
