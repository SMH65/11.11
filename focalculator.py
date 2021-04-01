import cv2
CAM_ID = 0
img_name = 0

cap = cv2.VideoCapture(CAM_ID)

while True:
    ret, frame = cap.read()

    if not ret:
        print("CAM is not available. Please check the port.")
        break

    key = cv2.waitKey(1)

    if key == 27:
        break

    if key == 13:
        cv2.imwrite('%d.png' %img_name, frame)
        print("img captured! ==> img number %d" %img_name)
        img_name = img_name + 1

    cv2.namedWindow("capture", cv2.WINDOW_NORMAL)
    cv2.imshow('capture', frame)



if cap.isOpened():
    cap.release()

cv2.destroyAllWindows()

# enter = 13
# esc = 27
# D = 100
# A = 97
# W = 119
# S = 115