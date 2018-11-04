import cv2
import numpy as np


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



def find_ColorThings(frame, color, num, RETR=cv2.RETR_EXTERNAL):
    mask = find_mask(frame, color)

    mask = cv2.dilate(mask, None, iterations=1)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
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


def find_center(BinThings_show, BinThings, contours):
    i = contours.index(max(contours, key=cv2.contourArea))  # 列表最大数的 索引
    # contours[i] = cv2.convexHull(contours[i])  # 不能是引用外包的填充方法，外面的线条会干扰 凸包的生成
    img01 = cv2.drawContours(BinThings, contours, i, (0, 0, 255), -1)
    cv2.imshow("img01", img01)

    img01 = cv2.cvtColor(img01, cv2.COLOR_BGR2GRAY)
    dist = cv2.distanceTransform(img01, cv2.DIST_L2, 3)  # 单通道灰度图才可以转化成 彩色图不行
    dist_output = cv2.normalize(dist, 0, 1.0, cv2.NORM_MINMAX)
    cv2.imshow("distance-t", dist_output*50)

    # ret, surface = cv2.threshold(dist, 1, dist.max()*0.5, cv2.THRESH_BINARY)
    ret, surface = cv2.threshold(dist,  dist.max() * 0.85, 255, cv2.THRESH_BINARY)  # 只保留中心点周围的图

    surface_fg = np.uint8(surface)
    BinThings, contours, hierarchy = cv2.findContours(surface_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    print("asdf", len(contours))
    x_list = []  # 中心的x坐标
    y_list = []  # 中心的y坐标
    center = []
    for k in range(len(contours)):
        cnt = contours[k]
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        x_list.append(cx)
        y_list.append(cy)
        center.append((cx, cy))
    print("before center is :", center)
    part = 0.5  # 边缘部分比例大于part的都需要找出（返回中心坐标和半径）
    if np.var(x_list, axis=0) > np.var(y_list, axis=0):  # 横向有多个图标，找到半径
        print(" heng " * 10)
        center = sorted(center, key=lambda x: x[0])   # 升序排列
        radius = int((center[-1][0] - center[0][0]) / (2 * (len(contours) - 1)))
        if center[0][0] - radius > 2 * part * radius:  # 左边有大半圆的话
            center.insert(0, (center[0][0] - 2 * radius, center[0][1]))
        if BinThings.shape[1] - center[-1][0] - radius > 2 * part * radius:   # 有边有大半圆的话
            center.append((center[-1][0] + 2 * radius, center[-1][1]))
    else:
        print(" shu " * 10)
        center = sorted(center, key=lambda x: x[1])  # 升序排列
        radius = int((center[-1][1] - center[0][1]) / (2 * (len(contours) - 1)))
        if center[0][1] - radius > 2 * part * radius:  # 上边有大半圆的话
            center.insert(0, (center[0][0], center[0][1] - 2 * radius))
        if BinThings.shape[0] - center[-1][1] - radius > 2 * part * radius:   # 下边有大半圆的话
            center.append((center[-1][0], center[-1][1] + 2 * radius))


    for i in range(len(center)):
        cv2.circle(BinThings_show, center[i], int(radius), (0, 0, 255), 2)  # 画圆
    cv2.imshow("BinThings_show",  BinThings_show)
    print("after center is :", center)
    cv2.waitKey(0)
    return center, radius


def watershed(img_path):
    SomeThings = cv2.imread(img_path)
    BinThings_show = SomeThings.copy()
    BinThings, BinColors, contours, hierarchy = find_ColorThings(SomeThings, "red",  num=0)
    print(BinThings.shape)

    center, radius = find_center(BinThings_show, BinThings, contours)
    #
    # blurred = BinThings
    # blurred = cv2.pyrMeanShiftFiltering(BinThings, 10, 100)
    # gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("~binary image:", ~binary)

    # binary = ~binary.copy()

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # mb = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=3)
    #
    # sure_bg = cv2.dilate(mb, kernel, iterations=1)  # 填充
    # cv2.imshow("mor-opt:", sure_bg)

    # circles = cv2.HoughCircles(sure_bg, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    # circles = np.uint8(np.around(circles))
    # for i in circles[0, :]:
    #     cv2.circle(BinThings, (i[0], i[1]), i[2], (0, 0, 255), 2)
    #     cv2.circle(BinThings, (i[0], i[1]), 2, (255, 0, 0), 2)
    # cv2.imshow("circle", circles)
    # contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)


if __name__ == "__main__":

    img_path = 'C:\\Users\\young\\Desktop\\just\\2000\\051.png'
    watershed(img_path)