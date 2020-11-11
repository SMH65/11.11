import cv2

capture = cv2.VideoCapture(0)
#variable = cv2.VideosCapture(channel_number)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow("VideoFrame", frame)
    cv2.namedWindow("VideoFrame", cv2.WINDOW_NORMAL)
    if cv2.waitKey(1) > 0: break

capture.release()
cv2.destroyAllWindows()