import cv2

src = cv2.imread("dir/lena.tif", cv2.IMREAD_COLOR)
height, width, channel = src.shape
print(height, width)

dst = src.copy()
dst = src[100:300, 200:400]
# height, width

cv2.imshow("src", src)
cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()