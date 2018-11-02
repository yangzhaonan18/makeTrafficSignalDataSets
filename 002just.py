import cv2
import numpy as  np


img = cv2.imread("C:\\Users\\young\\Desktop\\just\\2000\\996.png", 1)

cv2.imshow("asdf", img)
rows, cols, channel = img.shape
print(type(rows))
x = 50
pts1 = np.float32([[0, 0], [0, 242], [186, 0]])
pts2 = np.float32([[-54, -5], [x-50, 500], [186, -600]])

M = cv2.getAffineTransform(pts1, pts2)
dst = cv2.warpAffine(img, M, (cols+x, rows))

cv2.imshow("img:", dst)
cv2.waitKey(0)
