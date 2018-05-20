# -*- coding: utf-8 -*-
'''
WebカメラでキャプってAVIファイルにする。
'''

import cv2
import time

ESC_KEY = 27   # Escキー
DEVICE_ID = 0

cap = cv2.VideoCapture(DEVICE_ID)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('cap.avi', fourcc, 10.0, (640, 480))

# キャプチャ開始
while (cap.isOpened()):
    last_time = time.time()
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow('frame', frame)
        # Escキーで終了
        key = cv2.waitKey(1)
        if key == ESC_KEY:
            break
    else:
        break
    # FPS
    print('fps: {0}'.format(1 / (time.time() - last_time)))


# 後片付け
cap.release()
out.release()
cv2.destroyAllWindows()
