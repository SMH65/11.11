import cv2

src = cv2.imread("dir/bird.jpg", cv2.IMREAD_REDUCED_COLOR_4)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
ret, dst = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
ret, dst0 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

cv2.imshow("dst", dst)
cv2.imshow("dst0", dst0)
cv2.waitKey(0)
cv2.destroyAllWindows()