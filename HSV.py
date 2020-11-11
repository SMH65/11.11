import cv2
import numpy as np

src = cv2.imread("dir/HSV.jpg", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
# Hue, Saturation, Value

# color split
h = cv2.inRange(h, 40, 80)
print(h)
np.savetxt('data.txt', h)
orange = cv2.bitwise_or(hsv, hsv, mask = h)
orange = cv2.cvtColor(orange, cv2.COLOR_HSV2BGR)
cv2.imshow("orange", orange)
cv2.imshow("orgin", src)
cv2.imshow("mask", h)
# channel split
# cv2.imshow("h", h)
# cv2.imshow("s", s)
# cv2.imshow("v", v)


cv2.waitKey(0)
cv2.destroyAllWindows()

