import cv2
import numpy as np

# 1111111111111111111111
# 提取水平线 提取垂直线
# hline = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1), (-1, -1))  # 提取水平线
# vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20), (-1, -1))   # 提取垂直线 # 40 需要调
# temp = cv2.erode(binary_src, hline)    # 这两步就是形态学的开操作——先腐蚀再膨胀
# dst = cv2.dilate(temp, hline)
# dst = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vline)
# dst = cv2.bitwise_not(dst)
# cv2.imshow("Final image", dst)
# cv2.waitKey(0)


# 222222222222222222222222222222222222222
# if radius > 2:  # 只有当半径大于10时，才执行画图
#     cv2.circle(SomeThings, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # 画圆
#     cv2.circle(SomeThings, (int(x), int(y)), 5, (255, 255, 255), -1)  # 画质点
#     cv2.circle(SomeThings, center, 5, (0, 0, 0), -1)  # 画质点
#     cv2.circle(SomeThings, (5, 5), 5, (255, 0, 0), 3)
#     pts.appendleft(center)  # 把质心添加到pts中，并且是添加到列表左侧

# 3333333333333333333333333333333333333
#     # # 区域拟合直线
#     # rows, cols = SomeThings.shape[:2]
#     # [vx, vy, x, y] = cv2.fitLine(cnt_max, cv2.DIST_L2, 0, 0.01, 0.01)
#     # print("[vx, vy, x, y] :", [vx, vy, x, y])
#     # lefty = int((-x * vy / vx) + y)
#     # righty = int(((cols - x) * vy / vx) + y)
#     # SomeThings = cv2.line(SomeThings, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
#
#     # SomeThings = cv2.drawContours(SomeThings, contours, -1, (0, 255, 0), 1)  # 画边框
#     cv2.imshow('SomeThings',  SomeThings)
#     k = cv2.waitKey(0)
#     if k == 27:
#         break
#


i = 9
j = i
j = 7

print(j, i)