import numpy as np
import cv2
import matplotlib.pyplot as plt

cam_id = 0 #여기는 캠코더의 번호를 의미한다.
cap = cv2.VideoCapture(cam_id)
#cv2는 영상처리 모듈의 이름, VideoCapture함수는 cam_id의 영상 정보를 가져온다.

time = []
disp = []
data = []
FPS = 30
frm = 0

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 1,
                       qualityLevel = 0.1,
                       minDistance = 30,
                       blockSize = 14)

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 0,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some colors variables
color = np.random.randint(0,255,(100,3))
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)

# # Take first frame and find corners in it by Shitomasi
# ret, old_frame = cap.read()
# old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
# p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Take first frame and find coeners in it by ORB
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create(nfeatures=2)
kp, des = orb.detectAndCompute(old_gray, None)
p0 = cv2.KeyPoint_convert(kp)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
while(1):
    ret,frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # # Select good points (Shitomasi)
    # good_new = p1[st==1]
    # good_old = p0[st==1]

    # Select good points (ORB)
    good_new = p1
    good_old = p0


    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    data.append(b)
    disp = data[0] - data
    time.append(frm / FPS)
    frm = frm + 1

    img = cv2.add(frame,mask)
    img = cv2.flip(img, 1)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
cv2.destroyAllWindows()

plt.plot(time, disp, color='orange')
plt.show()