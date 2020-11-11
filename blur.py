import cv2

src = cv2.imread("dir/lena.tif", cv2.IMREAD_COLOR)

dst = cv2.blur(src, (1, 1), anchor=(-1, -1), borderType=cv2.BORDER_DEFAULT)

cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()