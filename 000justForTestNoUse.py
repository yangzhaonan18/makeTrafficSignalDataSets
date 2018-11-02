# import cv2
# import numpy as np
print(int(-1))
# # 1111111111111111111111
# # 提取水平线 提取垂直线
# # hline = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1), (-1, -1))  # 提取水平线
# # vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20), (-1, -1))   # 提取垂直线 # 40 需要调
# # temp = cv2.erode(binary_src, hline)    # 这两步就是形态学的开操作——先腐蚀再膨胀
# # dst = cv2.dilate(temp, hline)
# # dst = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vline)
# # dst = cv2.bitwise_not(dst)
# # cv2.imshow("Final image", dst)
# # cv2.waitKey(0)
#
#
# # 222222222222222222222222222222222222222
# # if radius > 2:  # 只有当半径大于10时，才执行画图
# #     cv2.circle(SomeThings, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # 画圆
# #     cv2.circle(SomeThings, (int(x), int(y)), 5, (255, 255, 255), -1)  # 画质点
# #     cv2.circle(SomeThings, center, 5, (0, 0, 0), -1)  # 画质点
# #     cv2.circle(SomeThings, (5, 5), 5, (255, 0, 0), 3)
# #     pts.appendleft(center)  # 把质心添加到pts中，并且是添加到列表左侧
#
# # 3333333333333333333333333333333333333
# #     # # 区域拟合直线
# #     # rows, cols = SomeThings.shape[:2]
# #     # [vx, vy, x, y] = cv2.fitLine(cnt_max, cv2.DIST_L2, 0, 0.01, 0.01)
# #     # print("[vx, vy, x, y] :", [vx, vy, x, y])
# #     # lefty = int((-x * vy / vx) + y)
# #     # righty = int(((cols - x) * vy / vx) + y)
# #     # SomeThings = cv2.line(SomeThings, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
# #
# #     # SomeThings = cv2.drawContours(SomeThings, contours, -1, (0, 255, 0), 1)  # 画边框
# #     cv2.imshow('SomeThings',  SomeThings)
# #     k = cv2.waitKey(0)
# #     if k == 27:
# #         break
# #
# # contours = [4,5,6,1,3,9]
# # contours.sort(key=lambda cnt:  cnt, reverse=True)
# # print(contours)
#
#
# # import cv2
# # import numpy as np
# # from matplotlib import pyplot as plt
# #
# # img = cv2.imread('C:\\Users\\young\\Desktop\\messi5.png', 0)
# # img2 = img.copy()
# # template = cv2.imread('C:\\Users\\young\\Desktop\\temp.jpg', 0)
# # w, h = template.shape[::-1]
# #
# # # All the 6 methods for comparison in a list
# # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
# #            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
# #
# # for meth in methods:
# #     img = img2.copy()
# #     method = eval(meth)
# #
# #     # Apply template Matching
# #     res = cv2.matchTemplate(img, template, method)
# #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# #
# #     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
# #     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
# #         top_left = min_loc
# #     else:
# #         top_left = max_loc
# #     bottom_right = (top_left[0] + w, top_left[1] + h)
# #
# #     cv2.rectangle(img, top_left, bottom_right, 255, 10)
# #
# #     plt.subplot(121), plt.imshow(res, cmap='gray')
# #     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# #     plt.subplot(122), plt.imshow(img, cmap='gray')
# #     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# #     plt.suptitle(meth)
# #
# #     plt.show()
#
#
# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
#
# path01 = 'C:\\Users\\young\\Desktop\\messi5.png'  # queryImage
# path02 = 'C:\\Users\\young\\Desktop\\temp.jpg'  # trainImage
# import cv2
# import numpy as np
#
# SZ = 20
# bin_n = 16  # Number of bins
#
# svm_params = dict(kernel_type=cv2.ml.SVM_LINEAR, svm_type=cv2.ml.SVM_C_SVC, C=2.67, gamma=5.383)
#
# affine_flags = cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR
#
#
# def deskew(img):
#     m = cv2.moments(img)
#     if abs(m['mu02']) < 1e-2:
#         return img.copy()
#     skew = m['mu11'] / m['mu02']
#     M = np.float32([[1, skew, -0.5 * SZ * skew], [0, 1, 0]])
#     img = cv2.warpAffine(img, M, (SZ, SZ), flags=affine_flags)
#     return img
#
#
# def hog(img):
#     gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
#     gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
#     mag, ang = cv2.cartToPolar(gx, gy)
#     bins = np.int32(bin_n * ang / (2 * np.pi))  # quantizing binvalues in (0...16)
#     bin_cells = bins[:10, :10], bins[10:, :10], bins[:10, 10:], bins[10:, 10:]
#     mag_cells = mag[:10, :10], mag[10:, :10], mag[:10, 10:], mag[10:, 10:]
#     hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
#     hist = np.hstack(hists)  # hist is a 64 bit vector
#     return hist
#
#
# # img = cv2.imread('digits.png', 0)
# img = cv2.imread("C:\\Users\\young\\Desktop\\temp.jpg", 0)
# img = cv2.resize(img, (50, 50), interpolation=cv2.INTER_CUBIC)
# cells = [np.hsplit(row, 100) for row in np.vsplit(img, 50)]
#
# # First half is trainData, remaining is testData
# train_cells = [i[:50] for i in cells]
# test_cells = [i[50:] for i in cells]
#
# ######     Now training      ########################
#
# deskewed = [map(deskew, row) for row in train_cells]
# hogdata = [map(hog, row) for row in deskewed]
# trainData = np.float32(hogdata).reshape(-1, 64)
# responses = np.float32(np.repeat(np.arange(10), 250)[:, np.newaxis])
#
# svm = cv2.SVM()
# svm.train(trainData, responses, params=svm_params)
# svm.save('svm_data.dat')
# #
# # ######     Now testing      ########################
# #
# # deskewed = [map(deskew, row) for row in test_cells]
# # hogdata = [map(hog, row) for row in deskewed]
# # testData = np.float32(hogdata).reshape(-1, bin_n * 4)
# # result = svm.predict_all(testData)
# #
# # #######   Check Accuracy   ########################
# # mask = result == responses
# # correct = np.count_nonzero(mask)
# # print (correct * 100.0 / result.size)
