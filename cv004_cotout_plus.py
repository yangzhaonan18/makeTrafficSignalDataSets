# -*- coding:utf-8 -*-

from collections import deque
import os
import cv2
import numpy as np
import random


def cal_xy(frame, x, y, radius):
    x1 = x - radius if x - radius > 0 else 0
    x2 = x + radius if x + radius < frame.shape[1] else frame.shape[1]  # cv里面横坐标是x 是shape[1]
    y1 = y - radius if y - radius > 0 else 0
    y2 = y + radius if y + radius < frame.shape[0] else frame.shape[0]  # cv里面纵坐标是y 是shape[0]
    return int(x1), int(x2), int(y1), int(y2)


def find_mask(frame, color):
    redLower01 = np.array([0, 80, 120])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([15, 255, 255])
    redLower02 = np.array([160, 80, 120])
    redUpper02 = np.array([179, 255, 255])

    yellowLower = np.array([5, 43, 46])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了

    greenLower = np.array([35, 80, 150])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([120, 255, 255])  # V 60 调整到了150

    blackLower = np.array([0, 0, 0])  # 黑色的阈值 标准H：0:180 S:0:255 V:0:46
    blackUpper = np.array([180, 250, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    r1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
    r2_mask = cv2.inRange(hsv, redLower02, redUpper02)

    r_mask = r1_mask + r2_mask
    y_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
    g_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域
    b_mask = cv2.inRange(hsv, blackLower, blackUpper)  # 根据阈值构建掩膜,黑色的区域
    if color == 0:
        mask = r_mask
    elif color == 1:
        mask = y_mask
    elif color == 2:
        mask = g_mask
    elif color == 3:
        mask = b_mask
    else:
        mask = None
    return mask


def find_ColorThings(frame, color, num):
    mask = find_mask(frame, color)
    mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    mask = cv2.dilate(mask, None, iterations=1)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    ColorThings = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # cv2.imshow("%d SomeThings:1R2G3B" % k, SomeThings)  # 显示感兴趣的颜色区域

    dst = cv2.GaussianBlur(ColorThings, (5, 5), 0)  # 高斯消除噪音
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)

    ret, SomeBinary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, heriachy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    cloneImage, contours, heriachy = cv2.findContours(SomeBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    return ColorThings, SomeBinary, contours



def add_line(ColorThings, x, y, radius):
    x = int(x)
    y = int(y)
    x1, x2, y1, y2 = cal_xy(ColorThings, x, y, radius)
    # 画矩形框
    # cv2.circle(ColorThings, (x, y), int(radius), (0, 255, 255), 2)  # 画圆
    # cv2.rectangle(ColorThings, (x1, y1), (x, y), (0, 0, 255), 2)  # 左上
    # cv2.rectangle(ColorThings, (x, y1), (x2, y), (0, 0, 255), 2)  # 右上
    # cv2.rectangle(ColorThings, (x1, y), (x, y2), (0, 0, 255), 2)  # 左下
    # cv2.rectangle(ColorThings, (x, y), (x2, y2), (0, 0, 255), 2)  # 右下
    return ColorThings


def cal_point(SomeBinary, x, y, radius):  # 返回最大方向的编号int
    x = int(x)
    y = int(y)
    x1, x2, y1, y2 = cal_xy(SomeBinary, x, y, radius)
    S00 = SomeBinary[y1:y, x1:x]  # 计算面积时，使用二值图，左上
    S01 = SomeBinary[y1:y, x:x2]  # 右上
    S10 = SomeBinary[y:y2, x1:x]  # 左下
    S11 = SomeBinary[y:y2, x:x2]  # 右下
    # print(S00.shape)  # (56, 56)
    # print(S01.shape)  # (56, 56)
    # print(S10.shape)  # (56, 56)
    # print(S11.shape)  # (56, 56)
    SS00 = np.sum(S00)
    SS01 = np.sum(S01)
    SS10 = np.sum(S10)
    SS11 = np.sum(S11)

    up_value = SS00 + SS01
    down_value = SS10 + SS11
    right_value = SS01 + SS11
    left_value = SS00 + SS10

    value = [left_value, up_value, right_value, down_value]
    if SS00 > SS11 and SS10 > SS01:
        return 1  # left
    elif SS00 > SS11 and SS01 > SS10:
        return 2  # 向上
    elif SS00 < SS11 and SS10 < SS01:
        return 3  # right
    elif SS00 < SS11 and SS01 < SS01:
        return 4
    else:
        direct_index = np.argmax(value)
        return direct_index + 1


def judge_index(ColorThings, contours, color, min_s, max_s, max_item):
    solidity = 0.85
    direct_index = 4
    ilter_num = 0
    while solidity > min_s and solidity < max_s and ilter_num < max_item:
        cnts = np.array(contours[0])

        for i in range(1, len(contours)):
            cnts = np.insert(cnts, 0, values=contours[i], axis=0)  # 添加其他的点

        # hull = cv2.convexHull(cnts)  # 轮廓转成凸包
        # ColorThings_line = ColorThings
        # cv2.polylines(ColorThings_line, [hull], True, (0, 0, 255), 2)  # 3.绘制凸包
        # #
        # rect = cv2.minAreaRect(cnts)  # 外接矩形
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)

        # 拟合直线
        # cv2.drawContours(ColorThings_line, [box], 0, (0, 0, 255), 2)
        # rows, cols = ColorThings_line.shape[:2]
        # [vx, vy, x, y] = cv2.fitLine(cnts, cv2.DIST_L2, 0, 0.01, 0.01)
        # print("[vx, vy, x, y] :", [vx, vy, x, y])
        # lefty = int((-x * vy / vx) + y)
        # righty = int(((cols - x) * vy / vx) + y)
        # ColorThings_line = cv2.line(ColorThings_line, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
        # ColorThings_line = cv2.drawContours(ColorThings_line, contours, -1, (0, 255, 0), 1)  # 画边框

        ((x, y), radius) = cv2.minEnclosingCircle(cnts)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
        x = int(x)
        y = int(y)
        # ColorThings_line = add_line(ColorThings_line, x, y, radius)  # 添加一些划分图形的直线和外接圆
        area = cv2.contourArea(cnts)  # 轮廓面积
        hull = cv2.convexHull(cnts)  # 计算出凸包形状(计算边界点)

        hull_area = cv2.contourArea(hull)  # 计算凸包面积
        solidity = float(area) / hull_area
        if solidity > max_s:
            direct_index = 0
            break
        elif solidity < min_s:
            direct_index = 4
            # cv2.imshow("%d %fimput image" % (ilter_num, solidity), ColorThings_line)
            # cv2.waitKey(0)  # ********************************
            break
        cnts_ColorThings = ColorThings.copy()
        hull_ColorThings = ColorThings.copy()
        # cv2.imshow("image", ColorThings)
        # cv2.waitKey(0)  # ********************************
        cnts_ColorThings = cv2.drawContours(cnts_ColorThings, [cnts], -1, (255, 255, 255), -1)
        # cv2.imshow("image",  cnts_ColorThings)
        # cv2.waitKey(0)  # ********************************
        hull_ColorThings = cv2.drawContours(hull_ColorThings, [hull], -1, (255, 255, 255), -1)  #

        print(type(hull_ColorThings))
        bb = ~cnts_ColorThings & hull_ColorThings & ~ColorThings

        cv2.imshow("image", bb)
        cv2.waitKey(0)  # ********************************
        print("ff"*100)



        print("solidity:", solidity)
        print("ilter_num:", ilter_num)

        ilter_num += 1
        ColorThings, SomeBinary, contours = find_ColorThings(ColorThings, color, num=ilter_num)
        if len(contours) == 0:
            break
        # cv2.imwrite(save_path, SomeBinary)  # 保存修改像素点后的图片
        direct_index = cal_point(SomeBinary, x, y, radius)

        font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
        # cv2.destroyAllWindows()
        index_dict = {0: "circle", 1: "<- ", 2: "/\\", 3: "->", 4: "V"}
        cv2.putText(ColorThings, "%s %s %.02f" % (index_dict[direct_index], ilter_num, solidity), (5, 20), font, 0.8, (0, 0, 255), 2)  # 添加文字
        # cv2.imshow("%d %fimput image" % (ilter_num, solidity), BlackThings)
        # cv2.waitKey(0)  # ********************************

    return direct_index


def find_class_name(SquareThings, color):
    ColorThings, _, contours = find_ColorThings(SquareThings, color, num=1)
    min_s = 0.7
    max_s = 0.93
    if len(contours) > 0:
        direct_index = judge_index(ColorThings, contours, color, min_s=min_s, max_s=max_s,max_item=55)
        index_dict = {0: "circle", 1: "<- ", 2: "/\\", 3: "->", 4: "V"}
        print("direction:"*10, index_dict[direct_index])
    else:
        print("NONONOONON0 color %d:", color)


def contours_demo(img_path, save_path):
    mybuffer = 64
    pts = deque(maxlen=mybuffer)
    frame = cv2.imread(img_path)
    for color in [0, ]:  # 分别单独处理三个颜色的结果
        SomeThings, _, contours = find_ColorThings(frame, color, num=1)
        # cv2.imshow("SomeThings", SomeThings)
        # cv2.waitKey(0)  # ********************************

        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上？
        #     cv2.drawContours(frame, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        if len(contours) > 0:  # 如果存在轮廓
            for i in range(0, len(contours)):

                # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
                contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
                cnt_max = contours[i]
                print("type(contours):", type(contours))
                ((x, y), radius) = cv2.minEnclosingCircle(cnt_max)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
                x1, x2, y1, y2 = cal_xy(SomeThings, int(x), int(y), radius)

                SquareThings01 = SomeThings[y1:y2, x1:x2]  # 裁剪需要的部分
                SquareThings_resize = cv2.resize(SquareThings01, (200, 200), interpolation=cv2.INTER_CUBIC)

                font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体

                # cv2.destroyAllWindows()
                # cv2.imshow("imput image", SquareThings)
                # cv2.putText(SquareThings, "imput image", (5, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
                # cv2.waitKey(0)
                name = find_class_name(SquareThings_resize, color)

                cv2.putText(SquareThings_resize, name, (1, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
                cv2.imwrite(save_path, SquareThings_resize)  # 保存修改像素点后的图片

                # SquareThings = cv2.resize(SquareThings, (500, 500), interpolation=cv2.INTER_CUBIC)
                # cv2.destroyAllWindows()
                # cv2.imshow(name, SomeThings)
                # k = cv2.waitKey(0)
                # if k == 27:
                #     break
                # solidity = 0.85
                # num = 1
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
