# -*- coding:utf-8 -*-

from collections import deque
import os
import cv2
import numpy as np


def cal_rect_xy(box):  # box是倾斜矩阵四个点的坐标
    # # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
    # heigh = box[0][1] - box[1][1]
    # width = box[2][0] - box[1][0]
    # ((355.1850891113281, 389.43994140625), (92.04371643066406, 270.73419189453125), -0.7345210313796997)
    x1 = min(i[0] for i in box)
    x2 = max(i[0] for i in box)
    y1 = min(i[1] for i in box)
    y2 = max(i[1] for i in box)
    return int(x1), int(x2), int(y1), int(y2)  # 返回倾斜矩形的最小外接矩形的左上角和右下角的点坐标


def Crop_cnt(frame, cnt, Crop_num = 4):
    hull = cv2.convexHull(cnt)  # 找到凸包
    rect = cv2.minAreaRect(hull)  # 外接矩形
    box = cv2.boxPoints(rect)  # 将中心点宽度高度旋转角度的表示方法转为点坐标
    box = np.int0(box)
    cx1, cx2, cy1, cy2 = cal_rect_xy(box)
    CropThing = frame[cy1:cy2, cx1:cx2]
    x0 = box[0][0] - cx1
    y0 = box[0][1] - cy1
    x1 = box[1][0] - cx1
    y1 = box[1][1] - cy1
    x2 = box[2][0] - cx1
    y2 = box[2][1] - cy1
    x3 = box[3][0] - cx1
    y3 = box[3][1] - cy1
    w = box[2][0] - box[1][0]
    h = box[0][1] - box[1][1]


    x = 500
    pts1 = np.float32([[x1, y1], [x0, y0], [x2, y2]])
    pts2 = np.float32([[0, 0], [0, h], [w, 0]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(CropThing, M, (w, h))
    cv2.imshow("asdfdas", dst)
    cv2.waitKey(0)


    print("af", rect)
    # 这里需要将外接倾斜矩形 纠正成水平的（投影变换）

    # 先切分开图像成功多块

    # 原图上裁剪出含cnt凸包的部分

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))  # 垂直模糊
    ColorThings_er = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

    CropThing = 0

    return CropThing

def identify_light(SomeThings, cnt, color, min_s, max_s):
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
    SomeThings_line = SomeThings.copy()
    add_line(SomeThings_line, x, y, radius)
    cv2.imshow("firt SomeThings_line", SomeThings_line)
    cv2.waitKey(0)  # ********************************

    x1, x2, y1, y2 = cal_circle_xy(SomeThings, int(x), int(y), radius)
    SquareThings = SomeThings[y1:y2, x1:x2]  # 裁剪需要的部分
    SquareThings_resize = cv2.resize(SquareThings, (200, 200), interpolation=cv2.INTER_CUBIC)

    name = find_class_name(SquareThings_resize, color, min_s, max_s)

    font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
    cv2.putText(SquareThings_resize, name, (1, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
    cv2.imwrite(save_path, SquareThings_resize)  # 保存修改像素点后的图片

def cla_color_ratio(cnt):  # 计算颜色的比例 考虑 单个目标和多个目标的计算过程
    cnt_area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)  # 计算出凸包形状(计算边界点)
    hull_area = cv2.contourArea(hull)  # 计算凸包面积
    color_ratio = float(cnt_area) / hull_area
    return color_ratio



def cla_hw_rat(cnt):
    """

    :param cnt:
    :return:
    """
    # ((x, y), radius) = cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径

    # SomeThings_line = SomeThings.copy()
    # SomeThings_line =
    # cv2.imshow("SomeThings_line", SomeThings_line )

    rect = cv2.minAreaRect(cnt)  # 外接矩形
    box = cv2.boxPoints(rect)
    box = np.int0(box)  # 左下角的点开始计数，顺时针转
    # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
    heigh = box[0][1] - box[1][1]
    width = box[2][0] - box[1][0]
    print("\nheigh:", box[0][1] - box[1][1])  # heigh: 271
    print("width:", box[2][0] - box[1][0])  # width: 92
    if heigh < 2 or width < 2:
        print(" heigh < 2 or width < 2")
        return 0
    rat = max(heigh, width) / min(heigh, width)  # int(rat + 0.5) =  3
    hw_rat = int(rat + 0.5)  # 四舍五入取整
    print("rat:", rat)

    return hw_rat

def detection(frame, SomeThings, cnt, color):   # 判断是否是需要识别的对象 是返回1 否为0
    # 只有一个轮廓
    hw_ratio = cla_hw_rat(cnt)  # 判断外接矩形的长宽比例  不应该很大
    color_art = cla_color_ratio(cnt)  # 计算轮毂面积 与凸包面积的比例 不应该很大
    CropThing = Crop_cnt(frame, cnt)
    # cnts = divide_cnt(frame, cnt)
    if hw_ratio > 10:
        return 0
    else:
        flag = 0
        return "asdf"





    # cv2.drawContours(SomeThings_line, [box[0:2]], 0, (0, 0, 255), 2)   # 画外接矩形
    # cv2.imshow("minAreaRect(cnt)", SomeThings_line)
    # cv2.waitKey(0)




def cal_point(SomeBinary, x, y, radius): # 返回最大方向的编号int
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

        rect = cv2.minAreaRect(cnts)   # 外接矩形
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
        print("solidity:", solidity)
        print("ilter_num:", ilter_num)
        cv2.waitKey(0)  # ********************************
        cv2.imshow("BinThings:", BinThings)
        cv2.waitKey(0)  # ********************************

        ilter_num += 1
        ColorThings, SomeBinary, contours = find_ColorThings(ColorThings, color, num=ilter_num)
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        if not contours or cv2.contourArea(contours[0]) < 5:
            break

        # cv2.imwrite(save_path, SomeBinary)  # 保存修改像素点后的图片
        # cv2.imshow("%d %fimput image" % (ilter_num, solidity), BlackThings)
        # cv2.waitKey(0)  # ********************************

    return direct_index

def find_class_name(SquareThings, color, min_s, max_s):
    ColorThings, _, contours = find_ColorThings(SquareThings, color, num=1)
    contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
    if len(contours) > 0:
        direct_index = judge_index(ColorThings, contours, color, min_s=min_s, max_s=max_s, max_item=55)
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
    redUpper01 = np.array([15, 255, 255])
    redLower02 = np.array([125, 80, 80])  # 125 to 156
    redUpper02 = np.array([180, 255, 255])

    greenLower = np.array([35, 80, 46])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([99, 255, 255])  # V 60 调整到了150

    blueLower = np.array([100, 80, 80])
    blueUpper = np.array([124, 255, 255])

    yellowLower = np.array([5, 80, 46])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
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


def find_ColorThings(frame, color, num):
    mask = find_mask(frame, color)

    mask = cv2.dilate(mask, None, iterations=1)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    ColorThings = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # an_ColorThings = cv2.bitwise_not(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # cv2.imshow("an_ColorThings:", an_ColorThings)
    # cv2.waitKey(0)  # ********************************

    # cv2.imshow("%d SomeThings:1R2G3B" % k, SomeThings)  # 显示感兴趣的颜色区域

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取
    ColorThings_er = cv2.morphologyEx(ColorThings, cv2.MORPH_OPEN, kernel)

    # cv2.imshow("line-result", ColorThings_er)


    dst = cv2.GaussianBlur(ColorThings, (5, 5), 0)  # 高斯消除噪音
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)

    ret, SomeBinary = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, heriachy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    cloneImage, contours, heriachy = cv2.findContours(SomeBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    return ColorThings, SomeBinary, contours



def contours_demo(img_path, save_path, min_s, max_s):
    ans = None
    mybuffer = 64
    pts = deque(maxlen=mybuffer)
    frame = cv2.imread(img_path)
    for color in ["red",  "blue", "black", "red+blue", "green", "yellow", "green+yellow",]:  # 分别单独处理三个颜色的结果
        SomeThings, SomeBinary, contours = find_ColorThings(frame, color, num=0)  # num = 腐蚀的次数

        # cv2.imshow("firt SomeThings", SomeThings)
        #
        # kernel_01 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))   # 直线提取
        # kernel_02 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        # SomeThings = cv2.morphologyEx(SomeThings, cv2.MORPH_OPEN, kernel_01)
        # SomeThings = cv2.morphologyEx(SomeThings, cv2.MORPH_OPEN, kernel_02)
        # cv2.imshow("opencv-result", SomeThings)

        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上
        #     cv2.drawContours(SomeThings, contours, i, (255, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充

        # cv2.waitKey(0)  # ********************************
        # if 1 == 1:
        #     break
        contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
        # cv2.imshow("SomeThings", SomeThings)
        # cv2.waitKey(0)  # ********************************
        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上
        #     cv2.drawContours(frame, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充

        if len(contours) > 0:  # 如果存在轮廓
            # contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
            contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)  # 根据轮毂的面积降序排列
            for i in range(0, len(contours)):
                # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
                # print("len(contours):", len(contours))
                if cv2.contourArea(contours[i]) > 100:  # 面积判断
                    detection(frame, SomeThings, contours[i], color)  # 判断是否是 需要识别的对象， 是返回1 否为0
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