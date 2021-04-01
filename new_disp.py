import cv2
import datetime
import numpy as np
import time
from matplotlib import pyplot as plt

CAM_ID = 0  # 2번은 캠코더 1번은 웹캠

cap = cv2.VideoCapture(CAM_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
date = datetime.datetime.now()

frm = 1
green = (0, 225, 0)
red = (0, 0, 225)

lk_params = dict(winSize=(15, 15),
                 maxLevel=0,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

ret, old_frame = cap.read()
# ROI 지정
mouse_is_pressing = False

def mouse_callback(event,x, y,flags,param):
    global start_x, start_y, mouse_is_pressing, key, img_ROI, x_, y_

    img_result = old_frame.copy()

    if event == cv2.EVENT_LBUTTONDOWN:

        mouse_is_pressing = True
        start_x, start_y = x, y

        cv2.circle(img_result, (x, y), 10, (0, 0, 0), -1)

        cv2.imshow("PleaseDrag", img_result)

    elif event == cv2.EVENT_MOUSEMOVE:

        if mouse_is_pressing:
            cv2.rectangle(img_result, (start_x, start_y), (x, y), green, 3)
            cv2.imshow("PleaseDrag", img_result)


    elif event == cv2.EVENT_LBUTTONUP:

        mouse_is_pressing = False

        img_ROI = old_frame[start_y:y, start_x:x]
        # img_result[start_y:y, start_x:x] = img_ROI
        cv2.namedWindow("img_roi", cv2.WINDOW_NORMAL)
        cv2.imshow("img_roi", img_ROI)
        x_ = x
        y_ = y

while True:
    cv2.namedWindow("PleaseDrag", cv2.WINDOW_NORMAL)
    cv2.imshow("PleaseDrag", old_frame)
    cv2.setMouseCallback("PleaseDrag", mouse_callback)
    key = cv2.waitKey()
    if key == 27:
        cv2.destroyAllWindows()
        break

old_gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create()
kp, des = orb.detectAndCompute(old_gray, None)

p0 = cv2.KeyPoint_convert(kp)
# Create a mask image for drawing purposes
sample_len = 100
mask = np.zeros_like(img_ROI)

id_dat = []
t = []
disp = []
datay = []
datax = []

START_POINT = []
END_POINT = []
END = 0
START = 0
counter = 0
first_trigger = True
prevTime = 0

while frm <= sample_len:
    ret, frame = cap.read()

    frame_roi = frame[start_y:y_, start_x:x_]
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1
    good_old = p0

    # draw the tracks`

    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new
        id_dat.append([i, a])

    frm = frm + 1

id_dat = np.array(id_dat)
id_dat = id_dat.reshape(sample_len, len(good_new), 2)  # frame, id, elements
arr = np.zeros((len(good_new), sample_len))

for n in range(sample_len):
    for i in range(len(good_new)):
        arr[i][n] = id_dat[n][i][1]

std_arr = []
for i in arr:
    std_arr.append(np.std(i))

k = 0
feature_id = []

std_arr_dict = {i: std_arr[i] for i in range(0, len(std_arr))}


def f2(x):
    return x[1]


res = sorted(std_arr_dict.items(), key=f2)
keys = dict(res).keys()
keys_list = list(keys)

# if len(keys_list) < 10:
#     feature_id = keys_list[0:1]
#     feature_id = list(map(int, feature_id))
#
# if len(keys_list) >= 10:
#     feature_id = keys_list[0:10]
#     feature_id = list(map(int, feature_id))

for numb in keys_list[0:10]:
    print(std_arr_dict[numb])
    if std_arr_dict[numb] <= 0.03:
        feature_id.append(numb)

frm = 1
print('FeatureId', feature_id)

while True:
    ret, frame = cap.read()
    crop_video = frame[start_y:y_, start_x:x_]
    # out_only_Video.write(crop_video)
    # if ret == True:
    curTime = time.time()

    sec = curTime - prevTime
    prevTime = curTime
    fps = 1 / (sec)

    # 프레임 수를 문자열에 저장
    str = "Process time : %0.1f" % fps

    frame_roi = frame[start_y:y_, start_x:x_]
    frame_gray = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1
    good_old = p0

    # ([id(feature),x_coord,y_coord])
    point_dat = []
    # draw the tracks

    for i, (new, old) in enumerate(zip(good_new, good_old)):
        for id in feature_id:
            if i == id:
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (a, b), (c, d), green, 2)
                frame_roi = cv2.circle(frame_roi, (a, b), 5, red, -1)
                point_dat.append([i, a, b])  # i 번째 포인트 x,y


    img = cv2.add(frame_roi, mask)

    k = cv2.waitKey(1) & 0xff

    datay.append(np.mean(np.array(point_dat)[:, 2]))

    t.append(frm)
    disp.append(datay[0] - np.mean(np.array(point_dat)[:, 2]))

    frm = frm + 1


    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame', img)

    if k == 27:
        break
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cv2.destroyAllWindows()

plt.plot(t, disp, color = 'orange')

plt.savefig('result.png')

plt.show()

