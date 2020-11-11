import cv2

img = cv2.imread('dir/numb.png', cv2.IMREAD_GRAYSCALE)

ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()
