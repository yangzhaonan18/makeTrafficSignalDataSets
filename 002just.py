import cv2
import numpy as  np


img = cv2.imread("C:\\Users\\young\\Desktop\\just\\2000\\993.png", 1)

cv2.imshow("asdf", img)
rows, cols, channel = img.shape
print(type(rows))
x = 500
pts1 = np.float32([[0, 0], [0, 758], [1563, 0]])
pts2 = np.float32([[0, 0], [x, 758], [1563 - x, 0]])

M = cv2.getAffineTransform(pts1, pts2)
dst = cv2.warpAffine(img, M, (cols+50, rows))

cv2.imshow("img:", dst)
cv2.waitKey(0)
