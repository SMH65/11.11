import cv2
import numpy as np

# import module_name as user_name

img = cv2.imread('dir/lena.tif', cv2.IMREAD_REDUCED_COLOR_4)
# object_name = cv2.imread('directory', mode)
# mode => etc.
# cv2.IMREAD_GRAYSCALE
# cv2.IMREAD_COLOR
# cv2.IMREAD_ANYDEPTH
# cv2.IMREAD_ANYCOLOR
# cv2.IMREAD_REDUCED_GRAYSCALE_2
# cv2.IMREAD_REDUCED_GRAYSCALE_4
# cv2.IMREAD_REDUCED_GRAYSCALE_8
# cv2.IMREAD_REDUCED_COLOR_2
# cv2.IMREAD_REDUCED_COLOR_4
# cv2.IMREAD_REDUCED_COLOR_8

cv2.imshow('img', img)
#cv2.imshow('win_name', object_name)

cv2.waitKey()
# cv2.waitKey(time)
# if time == 0 or blank  ==>  before enter any key, window doesn't disappear

cv2.destroyAllWindows()
cv2.imwrite('dir/lena.png', img)
# cv2.imwrite(filename, image)
# you can change the format