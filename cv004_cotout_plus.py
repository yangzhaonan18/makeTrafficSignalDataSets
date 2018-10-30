# -*- coding:utf-8 -*-

from collections import deque
import os
import cv2
import numpy as np
import random


def find_mask(frame):
    redLower01 = np.array([0, 80, 120])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([15, 255, 255])
    redLower02 = np.array([160, 80, 120])
    redUpper02 = np.array([179, 255, 255])

    yellowLower = np.array([5, 43, 46])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了

    greenLower = np.array([35, 80, 60])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([120, 255, 255])

    blackLower = np.array([0, 0, 0])  # 黑色的阈值 标准H：0:180 S:0:255 V:0:46
    blackUpper = np.array([180, 250, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    r1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
    r2_mask = cv2.inRange(hsv, redLower02, redUpper02)

    r_mask = r1_mask + r2_mask
    y_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
    g_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域
    b_mask = cv2.inRange(hsv, blackLower, blackUpper)  # 根据阈值构建掩膜,黑色的区域
    return [r_mask, y_mask, g_mask, b_mask]


def find_ColorThings(frame, color, num=1):
    mask = find_mask(frame)[color]
    # print(mask)
    mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    mask = cv2.dilate(mask, None, iterations=num)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    ColorThings = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域
    return ColorThings

def find_class_name(SquareThings, color):
    ColorThings = find_ColorThings(SquareThings, color, num=1)
    # cv2.imshow("%d SomeThings:1R2G3B" % k, SomeThings)  # 显示感兴趣的颜色区域
    dst = cv2.GaussianBlur(ColorThings, (5, 5), 0)  # 高斯消除噪音
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)
    # cv2.waitKey(0)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, heriachy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    cloneImage, contours, heriachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    print("len(contours):", len(contours))
    if len(contours) > 0:
        area = 0
        hull_area = 0
        for cnt in contours:
            hull = cv2.convexHull(cnt)

            # ColorThings = cv2.cvtColor(ColorThings, cv2.COLOR_GRAY2BGR)  # 3.绘制凸包
            cv2.polylines(ColorThings, [hull], True, (0, 255, 0), 2)  # 3.绘制凸包

            cv2.destroyAllWindows()
            cv2.imshow("ColorThings", ColorThings)
            cv2.waitKey(0)

            # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
            # ((x, y), radius) = cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
            area += cv2.contourArea(cnt)  # 轮廓面积
            hull = cv2.convexHull(cnt)  # 计算出凸包形状(计算边界点)
            hull_area += cv2.contourArea(hull)  # 计算凸包面积
        solidity = float(area) / hull_area
        print("solidity:", solidity)

        ColorThings, max_index = judge_index(ColorThings)

        # cv2.destroyAllWindows()
        # cv2.imshow("ColorThings", ColorThings)
        # cv2.waitKey(0)

        name = find_index_name(max_index, solidity, min_s=0.3, max_s=0.9)
        print("num and solidity:" * 5, "1", solidity)
    # cv2.destroyAllWindows()
    # cv2.imshow("cloneImage", cloneImage)
    # k = cv2.waitKey(0)
    # # if k == 27:
    # #     break
    #
    # # M = cv2.moments(cnt_max)  # 计算轮廓的矩
    # # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))  # 计算质心
    # max_index = judge_index(frame, ColorThings, x, y, radius)
    # if solidity>  0.8 and solidity < 0.9:
    #     while solidity>  0.8 and solidity < 0.9:
    #         return " "

def find_index_name(index, solidity, min_s, max_s):

    index_dict = {0: "<- ", 1: "/|\\", 2: "->", 3: "\|/"}
    if solidity > max_s:
        name = "circle-%.2f" % solidity
    elif solidity < min_s:
        name = "abnormal-%.2f" % solidity
    else:
        name = '%s%.2f' % (index_dict[index], solidity)
    return name


def judge_index(SquareThings):
    """
    判断SomeThings区域的方向，并在frame中标记出来。
    :param SquareThings:
    :return: int 类型0：左，1：上，2：右，3：下
    """
    gray = cv2.cvtColor(SquareThings, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    _, SomeBinary = cv2.threshold(gray, 0, 100, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cv2.imwrite(save_path, SomeBinary)  # 保存修改像素点后的图片

    # x1 = int(x - radius) if int(x - radius) > 0 else 0
    # x2 = int(x + radius) if int(x + radius) < SquareThings.shape[1] else int(SquareThings.shape[1])  # cv里面横坐标是x 是shape[1]
    # y1 = int(y - radius) if int(y - radius) > 0 else 0
    # y2 = int(y + radius) if int(y + radius) < SquareThings.shape[0] else int(SquareThings.shape[0])  # cv里面纵坐标是y 是shape[0]

    x1 = 0
    y1 = 0
    x = int(SquareThings.shape[1] / 2)
    y = int(SquareThings.shape[0] / 2)
    x2 = SquareThings.shape[1]
    y2 = SquareThings.shape[0]

    x = int(x)
    y = int(y)
    S00 = SomeBinary[y1:y, x1:x]  # 计算面积时，使用二值图，左上
    S01 = SomeBinary[y1:y, x:x2]  # 右上
    S10 = SomeBinary[y:y2, x1:x]  # 左下
    S11 = SomeBinary[y:y2, x:x2]  # 右下
    # print(S00.shape)  # (56, 56)
    # print(S01.shape)  # (56, 56)
    # print(S10.shape)  # (56, 56)
    # print(S11.shape)  # (56, 56)
    up_value = np.sum(S00) + np.sum(S01) - np.sum(S10) - np.sum(S11) if np.sum(S00) + np.sum(S01) > np.sum(
        S10) + np.sum(S11) else 0
    down_value = np.sum(S10) + np.sum(S11) - np.sum(S00) - np.sum(S01) if np.sum(S10) + np.sum(S11) > np.sum(
        S00) + np.sum(S01) else 0
    right_value = np.sum(S01) + np.sum(S11) - np.sum(S00) - np.sum(S10) if np.sum(S01) + np.sum(S11) > np.sum(
        S00) + np.sum(S10) else 0
    left_value = np.sum(S00) + np.sum(S10) - np.sum(S01) - np.sum(S11) if np.sum(S00) + np.sum(S10) > np.sum(
        S01) + np.sum(S11) else 0

    value = [left_value, up_value, right_value, down_value]
    max_index = np.argmax(value)

    # 画矩形框
    cv2.rectangle(SquareThings, (x1, y1), (x, y), (0, 0, 255), 1)  # 左上
    cv2.rectangle(SquareThings, (x, y1), (x2, y), (0, 255, 0), 1)  # 右上
    cv2.rectangle(SquareThings, (x1, y), (x, y2), (255, 0, 0), 2)  # 左下
    cv2.rectangle(SquareThings, (x, y), (x2, y2), (0, 255, 255), 1)  # 右下
    return SquareThings, max_index

def contours_demo(img_path, save_path):
    mybuffer = 64
    pts = deque(maxlen=mybuffer)
    frame = cv2.imread(img_path)
    mask_list = find_mask(frame)
    # mask = r_mask + y_mask + g_mask
    k = 0
    color = 0
    for mask in mask_list[color]:  # 分别单独处理三个颜色的结果
        SomeThings = find_ColorThings(frame, color=0, num=1)
        # cv2.imshow("%d SomeThings:1R2G3B" % k, SomeThings)  # 显示感兴趣的颜色区域
        dst = cv2.GaussianBlur(SomeThings, (5, 5), 0)  # 高斯消除噪音
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
        # cv2.imshow("gray image", gray)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
        # cloneImage, contours, heriachy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
        cloneImage, contours, heriachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

        for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上？
            cv2.drawContours(frame, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充

        if len(contours) > 0:  # 如果存在轮廓

            cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
            ((x, y), radius) = cv2.minEnclosingCircle(cnt_max)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径

            x1 = int(x - radius) if int(x - radius) > 0 else 0
            x2 = int(x + radius) if int(x + radius) < frame.shape[1] else int(frame.shape[1])  # cv里面横坐标是x 是shape[1]
            y1 = int(y - radius) if int(y - radius) > 0 else 0
            y2 = int(y + radius) if int(y + radius) < frame.shape[0] else int(frame.shape[0])  # cv里面纵坐标是y 是shape[0]

            SquareThings01 = SomeThings[y1:y2, x1:x2]  # 裁剪需要的部分
            SquareThings_resize = cv2.resize(SquareThings01, (100, 100), interpolation=cv2.INTER_CUBIC)

            font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体

            # cv2.destroyAllWindows()
            # cv2.imshow("imput image", SquareThings)
            # cv2.putText(SquareThings, "imput image", (5, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
            # cv2.waitKey(0)
            name = find_class_name(SquareThings_resize, color)

            cv2.putText(SquareThings_resize, name, (1, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
            cv2.imwrite(save_path, SquareThings_resize)  # 保存修改像素点后的图片

            # SquareThings = cv2.resize(SquareThings, (500, 500), interpolation=cv2.INTER_CUBIC)
            cv2.destroyAllWindows()
            # cv2.imshow(name, SomeThings)
            # k = cv2.waitKey(0)
            # if k == 27:
            #     break
            # solidity = 0.85
            num = 1
            # while solidity > 0.8 and solidity < 0.94 and num < 5:  # 大于0.94的判断为圆形， 小于0.8的为三角形，中间的需要腐蚀处理

            # cv2.imwrite(save_path, SomeThings)  # 保存修改像素点后的图片
            # print("type(SomeThings):", type(SomeThings))
            # # print("type(frame):", type(frame))
            # print("SomeThings:", SomeThings)
            # cv2.imwrite(save_path, frame)  # 保存修改像素点后的图片
            # cv2.imwrite(save_path, dst)  # 保存修改像素点后的图片




if __name__ == "__main__":
    print("*************** Python ********")
    # img_path = 'C:\\Users\\young\\Desktop\\just\\2001 (315).png'
    # img_path = "C:\\Users\\young\\Desktop\\just\\2003\\004 (2).jpg"
    # img_path = 'C:\\Users\\young\\Desktop\\just\\2003-after\\2002 (255).png'
    # img_path = 'C:\\Users\\young\\Desktop\\just\\2001\\TSD-Signal-00207-00014.png'

    work_dir = "C:\\Users\\young\\Desktop\\just"
    img_dir = "2000"
    save_dir = "2000-after"

    img_dir = os.path.join(work_dir, img_dir)
    save_dir = os.path.join(work_dir, save_dir)
    img_list = os.listdir(img_dir)
    for img in img_list:
        img_path = os.path.join(img_dir, img)
        save_name = os.path.splitext(img)[0] + ".png"
        save_path = os.path.join(save_dir, save_name)
        # 处理每一张图片并保存
        print("**********************")
        contours_demo(img_path, save_path)

    # src = cv2.imread(img_path)
    # cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("imput image", src)
    # cv2.waitKey(0)
    print("Finish")
    #
    # cv2.destroyAllWindows()
