import numpy as np
import cv2 as cv
import pandas as pd
import datetime
import csv
import glob
import os
import time
from pytictoc import TicToc

isDragging = False                      # 마우스 드래그 상태 저장
x0, y0, w, h = -1,-1,-1,-1              # 영역 선택 좌표 저장
blue, red = (255,0,0),(0,0,255)
def onMouse(event,x,y,flags,param):     # 마우스 이벤트 핸들 함수  ---①
    global isDragging, x0, y0, img, x_start, x_end, y_start, y_end    # 전역변수 참조
    if event == cv.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼 다운, 드래그 시작 ---②
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv.EVENT_MOUSEMOVE:  # 마우스 움직임 ---③
        if isDragging:                  # 드래그 진행 중
            img_draw = frame1.copy()       # 사각형 그림 표현을 위한 이미지 복제
            cv.rectangle(img_draw, (x0, y0), (x, y), blue, 2) # 드래그 진행 영역 표시
            cv.imshow('img', img_draw) # 사각형 표시된 그림 화면 출력
    elif event == cv.EVENT_LBUTTONUP:  # 왼쪽 마우스 버튼 업 ---④
        if isDragging:                  # 드래그 중지
            isDragging = False
            w = x - x0                  # 드래그 영역 폭 계산
            h = y - y0                  # 드래그 영역 높이 계산
            print("x:%d, y:%d, w:%d, h:%d" % (x0, y0, w, h))
            if w > 0 and h > 0:         # 폭과 높이가 양수이면 드래그 방향이 옳음 ---⑤
                img_draw = frame1.copy()   # 선택 영역에 사각형 그림을 표시할 이미지 복제
                # 선택 영역에 빨간 사각형 표시
                cv.rectangle(img_draw, (x0, y0), (x, y), red, 2)
                cv.imshow('img', img_draw) # 빨간 사각형 그려진 이미지 화면 출력
                roi = frame1[y0:y0+h, x0:x0+w] # 원본 이미지에서 선택 영영만 ROI로 지정 ---⑥
                y_start = y0
                y_end = y0+h
                x_start = x0
                x_end = x0+w

                cv.imshow('cropped', roi)  # ROI 지정 영역을 새창으로 표시
                cv.moveWindow('cropped', 0, 0) # 새창을 화면 좌측 상단에 이동
                cv.imwrite('./cropped.jpg', roi)   # ROI 영역만 파일로 저장 ---⑦
                print("croped.")
            else:
                cv.imshow('img', frame1)  # 드래그 방향이 잘못된 경우 사각형 그림ㅇㅣ 없는 원본 이미지 출력
                print("좌측 상단에서 우측 하단으로 영역을 드래그 하세요.")

cap = cv.VideoCapture(0)
ret, frame1 = cap.read()
cv.imshow('img', frame1)
cv.setMouseCallback('img', onMouse) # 마우스 이벤트 등록 ---⑧
cv.waitKey()
cv.destroyAllWindows()
frame1 = frame1[y_start:y_end, x_start:x_end]
prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
fieldnames = ["FRAME", "DISP"]
date = datetime.datetime.now()
with open('dir/Buffer_%s년%s월%s일T_%s시%s분%s초.csv' % (
        date.year, date.month, date.day, date.hour, date.minute, date.second), 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

list_of_files = glob.glob(
    'dir/*')  # * means all if need specific format then *.csv
Buffer_file = max(list_of_files, key=os.path.getctime)


# print(abs(y_start-y_end))
y=np.zeros((abs(y_start-y_end),abs(x_start-x_end)),dtype=float)
# print('y shape:',np.shape(y))
# print(abs(y_start-y_end),abs(x_start-x_end))
prevTime = 0
Time = 0
t = TicToc()
while(1):
    t.tic()
    ret, frame2 = cap.read()
    cv.imshow('frame2', frame2)
    frame2 = frame2[y_start:y_end, x_start:x_end]
    next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    dx = flow[...,0]
    dy = flow[...,1]
    # print('dy shape:',np.shape(dy))
    ydist = np.mean(y)
    print(y)
    # print(ydist)
    with open(Buffer_file, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "FRAME": float(Time),
            "DISP": ydist.item()
        }
        csv_writer.writerow(info)
        csv_file.close()


    # mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])



    k = cv.waitKey(30) & 0xff
    t.toc()
    y = y + dy
    sec = t.tocvalue()
    Time = Time + sec

    hz = 1 / (sec)
    # print('hz: ', hz)
    if k == 27:
        break

cv.destroyAllWindows()