import os
from datetime import datetime
import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없음")
    exit()

i = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print(f"{i}: read 실패")
    else:
        mean = frame.mean()
        if (mean != 0) and (i > 200):
            break
    i += 1
    # time.sleep(0.1)

cap.release()

now = datetime.now().strftime('%Y%m%d%H%M%S')
filename_raw = os.path.join('./', f"{now}.jpg")
colored = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
# cv2.imwrite(filename_raw, frame)


# 저장
now = datetime.now().strftime('%Y%m%d%H%M%S')
filename_out = os.path.join('./', f"{now}_dot.jpg")
cv2.imwrite(filename_out, output)