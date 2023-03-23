import cv2
import numpy as np

img = cv2.imread("../image/bright_ird.png")

# gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# hist_img = cv2.equalizeHist(gray_img)

# cv2.imwrite('bird2.png', hist_img)

gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
equ = cv2.equalizeHist(img)
res = np.hstack((img,equ)) #stacking images side-by-side
cv2.imwrite('res.png',res)