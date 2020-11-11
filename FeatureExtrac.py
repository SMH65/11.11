import cv2

img = cv2.imread('dir/bird.jpg', cv2.IMREAD_REDUCED_COLOR_4)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow('img', img)
# cv2.waitKey()

# #Harris corner detection
# gray_img = np.float32(gray_img)
#
# dst = cv2.cornerHarris(gray_img, blockSize=2, ksize=3, k=0.0005) #img, kernelsize, degree of sobel differential, k value
#
# #dilate to mark the corners
# dst = cv2.dilate(dst, None)
# img[dst > 0.01 * dst.max()] = [0, 255, 0]
#
# cv2.imshow('harris_corner', img)
# cv2.waitKey()

# #Shi-Tomasi corner detection
# corners = cv2.goodFeaturesToTrack(gray_img, maxCorners=30, qualityLevel=0.09, minDistance=30)
# corners = np.float32(corners)
#
# for item in corners:
#      x, y = item[0]
#      cv2.circle(img, (x, y), 6, (0, 255, 0), -1)
#
# cv2.imshow('good_features', img)
# cv2.waitKey()

##SIFT (Scale-Invariant Feature Transform)
# sift = cv2.xfeatures2d.SIFT_create()
# kp, des = sift.detectAndCompute(gray_img, None)


# kp_img = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# cv2.imshow('SIFT', kp_img)
# cv2.waitKey()


##FAST algorithm for corner detection
# fast = cv2.FastFeatureDetector_create(90)
# fast.setNonmaxSuppression(False)
#
# kp = fast.detect(gray_img, None)
# kp_img = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0))
#
# cv2.imshow('FAST', kp_img)
# cv2.waitKey()

##ORB
# orb = cv2.ORB_create(nfeatures=100)
# kp, des = orb.detectAndCompute(gray_img, None)
#
# kp_img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255), flags=0)
#
#
# cv2.imshow('ORB', kp_img)
# cv2.waitKey()
