# -*- coding:utf-8 -*-

from collections import deque
import os
import cv2
import numpy as np




def divide_crop(CropThing, wh_ratio):
    ColorThings_divide = CropThing.copy()  # 显示图片
    cv2.imshow("divide_crop", ColorThings_divide)
    cv2.waitKey(0)

    # if wh_ratio[0] == 0:
    #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))  # 水平消除模糊
    #     dst_divid = cv2.morphologyEx(CropThing, cv2.MORPH_OPEN, kernel)
    #     cv2.imshow("dst_divid:", dst_divid)
    #     cv2.waitKey(0)
    # else:
    #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))  # 水平消除模糊
    #     dst_divid = cv2.morphologyEx(CropThing, cv2.MORPH_OPEN, kernel)
    #     cv2.imshow("dst_divid:", dst_divid)
    #     cv2.waitKey(0)

    return "asdfa"


def cal_rect_xy(box):  # box是倾斜矩阵四个点的坐标
    # # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
    # heigh = box[0][1] - box[1][1]
    # width = box[2][0] - box[1][0]
    # ((355.1850891113281, 389.43994140625), (92.04371643066406, 270.73419189453125), -0.7345210313796997)
    x1 = max(min(i[0] for i in box), 0)  # 外接矩形的点，可能在边框外面，即有可能出现负数。
    x2 = max(max(i[0] for i in box), 0)
    y1 = max(min(i[1] for i in box), 0)
    y2 = max(max(i[1] for i in box), 0)
    return int(x1), int(x2), int(y1), int(y2)  # 返回倾斜矩形的最小外接矩形的左上角和右下角的点坐标


def Crop_cnt(frame, cnt, wh_ratio):  # 裁剪轮廓凸包
    """
    :param frame:
    :param cnt:
    :return: CropThing 返回经过 旋转裁剪 后的图片
    """
    hull = cv2.convexHull(cnt)  # 找到凸包
    rect_min = cv2.minAreaRect(hull)  # 最小外接矩形
    x1, y1, w, h = cv2.boundingRect(hull)  # 外接矩形
    box01 = cv2.boxPoints(rect_min)  # 将中心点宽度高度旋转角度的表示方法转为点坐标
    box = np.int0(box01)  # 最小外接矩形

    ColorThings_line = frame.copy()  # 显示图片

    # cv2.rectangle(ColorThings_line, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)  # 画外接矩形
    # cv2.imshow("Crop_cnt: ", ColorThings_line)
    # print("box", type(box))  # box  <class 'numpy.ndarray'> [[178 488] [156 444] [322 363] [343 407]]
    # print("box:", box)

    print("wh_ratio", wh_ratio)
    if wh_ratio[1] == 1:  # 正方的图形，不需要纠正角度（很难判断是否是倾斜的）
        cv2.rectangle(ColorThings_line, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)  # 画最小外接矩形
        cv2.imshow("ColorThings_line", ColorThings_line)
        # cv2.waitKey(0)
        return frame[y1: y1 + h, x1:x1 + w]

    else:  # 长条的图形需要纠正倾斜
        cx1, cx2, cy1, cy2 = cal_rect_xy(box)
        CropThing = frame[cy1:cy2, cx1:cx2]  # 裁剪图片
        x0 = box[0][0] - cx1  # 最下面的那个点（首选左边的）
        y0 = box[0][1] - cy1
        x1 = box[1][0] - cx1
        y1 = box[1][1] - cy1
        x2 = box[2][0] - cx1
        y2 = box[2][1] - cy1
        x3 = box[3][0] - cx1
        y3 = box[3][1] - cy1
        w = box[2][0] - box[1][0]
        h = box[0][1] - box[1][1]
        print(x0, x1, x2, x3, y0, y1, y2, y3)
        rat = 1.1  # 缩放比例  利用三个坐标点透视变换 （特点：前后平行线保持平行）
        pts1 = np.float32([[x1, y1], [x0, y0], [x2, y2]])
        pts2 = np.float32([[0, 0], [0, int(h * rat)], [int(w * rat), 0]])
        # print("pts1, pts2", pts1, pts2)
        # print("(int(w * rat), int(h * rat)):", (int(w * rat), int(h * rat)))
        M = cv2.getAffineTransform(pts1, pts2)
        CropThing = cv2.warpAffine(CropThing, M, (int(w * rat), int(h * rat)))  # 纠正倾斜后的裁剪后图形
        cv2.drawContours(ColorThings_line, [box], 0, (0, 0, 255), 2)  # 画最小外接矩形
        cv2.imshow("ColorThings_line", ColorThings_line)
        # cv2.waitKey(0)
        # 这里需要将外接倾斜矩形 纠正成水平的（透视变换）
        # 先切分开图像成功多块
        # 原图上裁剪出含cnt凸包的部分
        return CropThing  # 返回裁剪下来的图片


def identify_light(SomeThings, cnt, color, min_s, max_s):
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
    SomeThings_line = SomeThings.copy()
    add_line(SomeThings_line, x, y, radius)
    cv2.imshow("firt SomeThings_line", SomeThings_line)
    # cv2.waitKey(0)  # ********************************

    x1, x2, y1, y2 = cal_circle_xy(SomeThings, int(x), int(y), radius)
    SquareThings = SomeThings[y1:y2, x1:x2]  # 裁剪需要的部分
    SquareThings_resize = cv2.resize(SquareThings, (200, 200), interpolation=cv2.INTER_CUBIC)

    name = find_class_name(SquareThings_resize, color, min_s, max_s)

    font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
    cv2.putText(SquareThings_resize, name, (1, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
    cv2.imwrite(save_path, SquareThings_resize)  # 保存修改像素点后的图片


def cal_color_area(BinColors, contours, hierarchy):  # 计算轮廓的面积。两个变量的长度是相同的，同一个图形的参数

    # print(type(hierarchy))  # <class 'numpy.ndarray'>  多维矩阵………还没有细看
    # print("hierarchy[0] = ", hierarchy[0])  # hierarchy[0] =  [[ 1 -1 -1 -1] [ 2  0 -1 -1]]
    # print("hierarchy[0][0][0] = ", hierarchy[0][0][0])  # hierarchy[0][0][0] =  1
    if len(contours) == 0:
        print("len(contours) == 0:")
        return -1
    if len(contours) == 1:
        print("len(contours) == 1:")
        return cv2.contourArea(contours[0])
    area_p = 0
    area_n = 0
    i = 0
    j = 0
    flag = 1
    BinColors_show = BinColors.copy()
    print("hierarchy =", hierarchy)
    while i != -1:  # 遍历第一层所有的轮廓的编号  cv2.RETR_CCOMP 保证包住白色的轮廓是第一层，包住黑色的是第二层
        print("i =", i)
        cv2.drawContours(BinColors_show, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        cv2.imshow("cal_color_area//BinColors_show", BinColors_show)
        area_p += cv2.contourArea(contours[i])
        if hierarchy[0][i][0] != i + 1 and flag == 1:
            j = i + 1
            flag = 0
        i = hierarchy[0][i][0]  # 同一层的编号是串联的，一个接一个
    print("area_p =", area_p)
    while j != -1 and j < len(contours):  # 遍历第二层所有的轮廓的编号
        print("j =", j)
        cv2.drawContours(BinColors_show, contours, j, (255, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        cv2.imshow("cal_color_area//BinColors_show", BinColors_show)
        area_n += cv2.contourArea(contours[j])

        j = hierarchy[0][j][0]
    print("area_n =", area_n)
    print("area_p - area_n =", area_p - area_n)
    return area_p - area_n


def cal_color_ratio(CropThing, color):  # 计算颜色的比例 考虑 单个目标和多个目标的计算过程 方法相同
    # cv2.imshow("cal_color_ratio/CropThing ", CropThing)  # 直接裁剪后，没有处理过的图片
    BinColors, BinThings, contours, hierarchy = find_ColorThings(CropThing, color, num=0, RETR=cv2.RETR_CCOMP)
    if len(contours) == 0:
        return -1
    color_area = cal_color_area(BinColors, contours, hierarchy)
    cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
    cnt_area = cv2.contourArea(cnt_max)  # 轮廓的面积 ？ 不能使用这个参数 判断不直观
    hull = cv2.convexHull(cnt_max)  # 计算出凸包形状(计算边界点)
    hull_area = cv2.contourArea(hull)  # 计算凸包面积
    if hull_area == 0:
        print("cal_color_ratio//hull_area == 0")
        return -1
    color_ratio = float(color_area) / hull_area
    cnt_ratio = float(cnt_area) / hull_area
    print("cal_color_ratio//hull_area", hull_area)
    print("cal_color_ratio//color_ratio", color_ratio)
    print("cal_color_ratio//cnt_ratio", cnt_ratio)

    CropThing_show = CropThing.copy()
    # for i in range(len(contours)):  [contours[3]]
    # cnts = contours[max_index]
    # cv2.drawContours(CropThing_show, [contours[3]], -1, (0, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充
    # cv2.imshow(" cal_color_ratio", CropThing_show)
    # cv2.waitKey(0)


    # CropThing_show = SomeBinary.copy()  # 这个图片只要红色
    # # cv2.drawContours(CropThing_show, contours, i, (0, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充
    #
    # cv2.namedWindow("cal_color_ratio:", 0)
    # cv2.resizeWindow("cal_color_ratio:", 640, 480)
    # cv2.imshow("cal_color_ratio:", CropThing_show)
    # cv2.waitKey(0)
    #

    return color_ratio


def cal_wh_ratio(cnt):
    # x, y, w, h = cv2.boundingRect(cnt)  # 外接矩形
    # cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 5)
    # cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
    # SomeThings_line = SomeThings.copy()
    # SomeThings_line =
    # cv2.imshow("SomeThings_line", SomeThings_line )
    rect = cv2.minAreaRect(cnt)  # 外接矩形
    box = cv2.boxPoints(rect)
    box = np.int0(box)  # 左下角的点开始计数，顺时针转
    # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
    heigh = box[0][1] - box[1][1]
    width = box[2][0] - box[1][0]

    if heigh < 10 or width < 10:  # 忽略低于10像素的 #################33？？？？？？？？？？？？？？？？？？？？？？？？
        print("heigh < 10 or width < 10")
        return [-1, -1]
    rat = max(heigh, width) / min(heigh, width)  # int(rat + 0.5) =  3
    wh_rat = int(rat + 0.5)  # 四舍五入取整
    if width > heigh:
        print("width > heigh", width, heigh)
        print("[0, hw_rat] =", [0, wh_rat])
        return [0, wh_rat]  # 0 表示图标是横向的
    else:
        print("width < heigh", width, heigh)
        print("[1, hw_rat] =", [1, wh_rat])
        return [1, wh_rat]  # 1 表示图标是纵向的


def detection(frame, BinColors, color, contours, i):  # 判断是否是需要识别的对象 是返回1 否为0
    # 输入只有一个轮廓
    BinColors_show = BinColors.copy()
    cv2.drawContours(BinColors_show, contours, i, (0, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
    cv2.imshow(" detection/BinColors_show", BinColors_show)

    wh_ratio = cal_wh_ratio(contours[i])  # 判断外接矩形的长宽比例   不应该很大
    CropThing = Crop_cnt(frame, contours[i], wh_ratio)  # 裁剪图片， 将图片变成水平的
    color_ratio = cal_color_ratio(CropThing, color)  # 计算轮廓面积 与 凸包面积的比例  不应该很大
    # print("asfasdfaaaaaaaaa", int(wh_ratio[1]))
    if wh_ratio[1] > 10:  # 特别长的不可能，
        print("case0: wh_ratio[1] > 10 or (wh_ratio[1] > 1 and color_ratio > 0.3 )", wh_ratio[1], wh_ratio[1], color_ratio)
        return -1
    if wh_ratio[1] > 1 and color_ratio > 0.8:  # 红色的比例不可能很高
        print("case1: detection//wh_ratio[1] > 1 and color_ratio > 0.9")
        return -1
    if wh_ratio[1] == 1 and color_ratio < 0.3:  # 正方的图形，只有可能是静止和红路灯 红色的比例不可能很低
        print("case2: wh_ratio[1] == 1 and color_ratio < 0.5", wh_ratio[1] == 1 and color_ratio < 0.5)
        return -1
    if color == "red" and wh_ratio[1] == 1 and color_ratio < 0.6:  # 正方的图形中，绿色的面积不应该很低
        return -1
    if wh_ratio[1] > 1:
        cnts = divide_crop(CropThing, wh_ratio)


    return 1

    # cv2.drawContours(SomeThings_line, [box[0:2]], 0, (0, 0, 255), 2)   # 画外接矩形
    # cv2.imshow("minAreaRect(cnt)", SomeThings_line)


def cal_point(SomeBinary, x, y, radius):  # 返回最大方向的编号int
    x = int(x)
    y = int(y)
    x1, x2, y1, y2 = cal_circle_xy(SomeBinary, x, y, radius)
    S00 = SomeBinary[y1:y, x1:x]  # 计算面积时，使用二值图，左上
    S01 = SomeBinary[y1:y, x:x2]  # 右上
    S10 = SomeBinary[y:y2, x1:x]  # 左下
    S11 = SomeBinary[y:y2, x:x2]  # 右下

    SS00 = np.sum(S00)
    SS01 = np.sum(S01)
    SS10 = np.sum(S10)
    SS11 = np.sum(S11)

    value = [SS00, SS01, SS10, SS11]
    value.sort(reverse=True)  # 将面积大的放在前面
    if SS01 in value[0:2] and SS11 in value[0:2]:  # 箭头右侧需要补齐的东西多
        return 1  # left
    elif SS10 in value[0:2] and SS11 in value[0:2]:
        return 2  # up
    elif SS00 in value[0:2] and SS10 in value[0:2]:
        return 3  # right
    elif SS00 in value[0:2] and SS01 in value[0:2]:
        return 4  # down
    else:
        direct_index = np.argmax(value)
        return direct_index + 1


def judge_index(ColorThings, contours, color, min_s, max_s, max_item):
    solidity = 0.85
    direct_index = 4
    ilter_num = 1
    while solidity > min_s and solidity < max_s and ilter_num < max_item:
        cnts = np.array(contours[0])
        # for i in range(1, len(contours)):
        #     if cv2.contourArea(contours[i]) > 25:
        #         cnts = np.insert(cnts, 0, values=contours[i], axis=0)  # 添加其他的点
        hull = cv2.convexHull(cnts)  # 轮廓转成凸包
        ColorThings_line = ColorThings.copy()
        cv2.polylines(ColorThings_line, [hull], True, (0, 0, 255), 2)  # 3.绘制凸包

        rect = cv2.minAreaRect(cnts)  # 外接矩形
        box = cv2.boxPoints(rect)

        # box = np.int0(box)
        # cv2.drawContours(ColorThings_line, [box], 0, (0, 0, 255), 2)   # 画外接矩形

        rows, cols = ColorThings_line.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(cnts, cv2.DIST_L2, 0, 0.01, 0.01)
        # print("[vx, vy, x, y] :", [vx, vy, x, y])
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        # ColorThings_line = cv2.line(ColorThings_line, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
        ColorThings_line = cv2.drawContours(ColorThings_line, contours, -1, (0, 255, 0), 1)  # 画边框
        ((x, y), radius) = cv2.minEnclosingCircle(cnts)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径

        x = int(x)
        y = int(y)
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
        cnts_ColorThings = cv2.drawContours(cnts_ColorThings, [cnts], -1, (255, 255, 255), -1)
        hull_ColorThings = cv2.drawContours(hull_ColorThings, [hull], -1, (255, 255, 255), -1)
        BinThings = ~cnts_ColorThings & hull_ColorThings & ~ColorThings
        direct_index = cal_point(BinThings, x, y, radius)

        font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
        # cv2.destroyAllWindows()
        index_dict = {0: "circle", 1: "<- ", 2: "/\\", 3: "->", 4: "V"}
        cv2.putText(ColorThings_line, "%s %s %.02f" % (index_dict[direct_index], ilter_num, solidity), (5, 20), font,
                    0.8, (0, 255, 255), 2)  # 添加文字
        cv2.imshow("ColorThings_line", ColorThings_line)
        # print("solidity:", solidity)
        # print("ilter_num:", ilter_num)
        # cv2.waitKey(0)  # ********************************
        # cv2.imshow("BinThings:", BinThings)
        # cv2.waitKey(0)  # ********************************

        ilter_num += 1
        BinThings, BinColors, contours, hierarchy = find_ColorThings(ColorThings, color, num=ilter_num)
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        if not contours or cv2.contourArea(contours[0]) < 5:
            break

        # cv2.imwrite(save_path, SomeBinary)  # 保存修改像素点后的图片
        # cv2.imshow("%d %fimput image" % (ilter_num, solidity), BlackThings)
        # cv2.waitKey(0)  # ********************************

    return direct_index


def find_class_name(SquareThings, color, min_s, max_s):
    BinColors, BinThings, contours, hierarchy = find_ColorThings(SquareThings, color, num=1)
    contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
    if len(contours) > 0:
        direct_index = judge_index(BinColors, contours, color, min_s=min_s, max_s=max_s, max_item=55)
        index_dict = {0: "circle", 1: "<- ", 2: "/\\", 3: "->", 4: "V"}
        print("direction:", index_dict[direct_index])
        return index_dict[direct_index]
    else:
        print("NONONOONON0 color %d:" % color)
        return "NONONOONON0 color %d:" % color


def cal_circle_xy(frame, x, y, radius):
    x1 = x - radius if x - radius > 0 else 0
    x2 = x + radius if x + radius < frame.shape[1] else frame.shape[1]  # cv里面横坐标是x 是shape[1]
    y1 = y - radius if y - radius > 0 else 0
    y2 = y + radius if y + radius < frame.shape[0] else frame.shape[0]  # cv里面纵坐标是y 是shape[0]
    return int(x1), int(x2), int(y1), int(y2)


def add_line(ColorThings, x, y, radius):
    x = int(x)
    y = int(y)
    x1, x2, y1, y2 = cal_circle_xy(ColorThings, x, y, radius)
    # 画矩形框
    cv2.circle(ColorThings, (x, y), int(radius), (0, 255, 255), 2)  # 画圆
    cv2.rectangle(ColorThings, (x1, y1), (x, y), (0, 0, 255), 2)  # 左上
    cv2.rectangle(ColorThings, (x, y1), (x2, y), (0, 0, 255), 2)  # 右上
    cv2.rectangle(ColorThings, (x1, y), (x, y2), (0, 0, 255), 2)  # 左下
    cv2.rectangle(ColorThings, (x, y), (x2, y2), (0, 0, 255), 2)  # 右下


def find_mask(frame, color):
    blackLower01 = np.array([0, 0, 0])  # 黑的阈值 标准H：0:180 S:0:255 V:0:46:220
    blackUpper01 = np.array([180, 255, 90])
    blackLower02 = np.array([0, 0, 46])  # 灰的阈值 标准H：0:180 S:0:43 V:0:46:220
    blackUpper02 = np.array([180, 43, 45])  # 灰色基本没用

    redLower01 = np.array([0, 80, 80])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([10, 255, 255])
    redLower02 = np.array([156, 80, 80])  # 125 to 156
    redUpper02 = np.array([180, 255, 255])

    greenLower = np.array([50, 80, 80])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([95, 255, 255])  # V 60 调整到了150

    blueLower = np.array([105, 120, 80])  # 蓝H:100:124 紫色H:125:155
    blueUpper = np.array([130, 255, 255])

    yellowLower = np.array([26, 80, 100])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
    red2_mask = cv2.inRange(hsv, redLower02, redUpper02)
    red_mask = red1_mask + red2_mask

    black01_mask = cv2.inRange(hsv, blackLower01, blackUpper01)  # 根据阈值构建掩膜,黑色的区域
    black02_mask = cv2.inRange(hsv, blackLower02, blackUpper02)  # 根据阈值构建掩膜,黑色的区域
    black_mask = black01_mask + black02_mask

    yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
    green_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域

    blue_mask = cv2.inRange(hsv, blueLower, blueUpper)
    if color == "black":
        mask = black_mask
    elif color == "yellow":
        mask = yellow_mask
    elif color == "red":
        mask = red_mask
    elif color == "green":
        mask = green_mask
    elif color == "blue":
        mask = blue_mask
    elif color == "red+blue":
        mask = red_mask + blue_mask
    elif color == "green+yellow":
        mask = green_mask + yellow_mask


    else:
        mask = None
    return mask


def find_ColorThings(frame, color, num, RETR=cv2.RETR_EXTERNAL):
    mask = find_mask(frame, color)

    mask = cv2.dilate(mask, None, iterations=2)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # an_ColorThings = cv2.bitwise_not(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # cv2.imshow("an_ColorThings:", an_ColorThings)
    # cv2.waitKey(0)  # ********************************

    # cv2.imshow("First BinColors",  BinColors)  # 显示感兴趣的颜色区域

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取    找到轮廓的时候忽略掉小目标 后续正确的小目标通过膨胀复原
    BinColors = cv2.morphologyEx(BinColors, cv2.MORPH_OPEN, kernel)

    # cv2.imshow("line-result", ColorThings_er)

    dst = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)

    ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    # cloneImage, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    BinThings, contours, hierarchy = cv2.findContours(BinThings, RETR, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 黑白图时 直线消除 小斑点
    BinThings = cv2.morphologyEx(BinThings, cv2.MORPH_OPEN, kernel)  # 输出是二值化的图片， 后面用来作为轮廓使用 吧！！！！！
    BinThings, contours, hierarchy = cv2.findContours(BinThings, RETR, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    ret, mask = cv2.threshold(BinThings, 190, 255, cv2.THRESH_BINARY)  # 二值图提取mask
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 二值化中白色对应的彩色部分
    # cv2.imshow("find_ColorThings/BinColors：", BinColors)
    return BinColors, BinThings, contours, hierarchy


def contours_demo(img_path, save_path, min_s, max_s):
    ans = None
    mybuffer = 64
    pts = deque(maxlen=mybuffer)
    frame = cv2.imread(img_path)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
    # frame = cv2.pyrMeanShiftFiltering(frame, 15, 15)  # 神奇 但5秒处理一张图
    # frame_best = frame.copy()
    # for color in ["red",  "blue", "black", "red+blue", "green", "yellow", "green+yellow",]:  # 分别单独处理三个颜色的结果
    for color in [ "red", "blue",  "green", "yellow"]:  # 分别单独处理三个颜色的结果

        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取
        # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

        BinColors, BinThings, contours, hierarchy = find_ColorThings(frame, color, num=0)  # num = 腐蚀的次数
        # SomeThings = cv2.pyrMeanShiftFiltering( SomeThings, 15, 15)
        #         # cv2.imshow("firt SomeThings", SomeThings)
        # SomeThings = cv2.GaussianBlur(SomeThings, (5, 5), 0)  # 高斯消除噪音

        # cv2.imshow("opencv-result", SomeThings)
        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上
        #     cv2.drawContours(SomeThings, contours, i, (255, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充

        # SomeBinary = cv2.bitwise_and(frame, SomeBinary)

        # cv2.waitKey(0)  # ********************************
        # if 1 == 1:
        #     break
        # contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)
        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上
        #     cv2.drawContours(frame, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        # cv2.imshow("SomeThings", SomeThings)
        # cv2.waitKey(0)  # ********************************

        if len(contours) < 1:  # 排除不存在轮廓的情况
            # contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
            print("len(contours) < 1 :", len(contours))
            continue
        contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)  # 根据轮毂的面积降序排列
        for i in range(0, len(contours)):
            # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
            # print("len(contours):", len(contours))
            if cv2.contourArea(contours[i]) < 50:  # 排除面积判断 < 50
                print("cv2.contourArea(contours[%d]) < 100 " % i, cv2.contourArea(contours[i]))
                continue
            detection(frame, BinColors, color, contours, i)  # 判断是否是 需要识别的对象， 是返回1 否为0
            # identify_light(SomeThings, contours[i], color, min_s, max_s)


if __name__ == "__main__":
    print("*************** Python ********")
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
        print("\n A nem img,img_path :%s" % img_path)
        # watershed(img_path)
        ans = contours_demo(img_path, save_path, min_s=0.7, max_s=0.93)
        print("ans")

    # src = cv2.imread(img_path)
    # cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("imput image", src)
    # cv2.waitKey(0)
    print("Finish")
    #
    # cv2.destroyAllWindows()
