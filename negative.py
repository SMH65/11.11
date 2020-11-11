import cv2

src = cv2.imread("dir/bird.jpg", cv2.IMREAD_REDUCED_COLOR_4)

dst = cv2.bitwise_not(src)

cv2.imshow("src", src)
cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()