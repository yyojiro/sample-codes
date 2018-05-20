# -*- coding: utf-8 -*-
'''
デスクトップをキャプってaviファイルに保存するだけの雑なサンプル。
PILよりmssを使うとよいらしい。
'''

import numpy as np
import cv2
import mss
import time

# キャプチャする領域
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

frame_rate = 30.0
frame_size = (960, 540)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('cap.avi',
                      fourcc,
                      frame_rate,
                      frame_size)

with mss.mss() as sct:
    while True:
        last_time = time.time()
        sct_img = np.array(sct.grab(monitor))
        # 半分にリサイズ
        half = cv2.resize(sct_img, (960, 540), interpolation=cv2.INTER_LINEAR_EXACT)
        # 変換
        img = cv2.cvtColor(half, cv2.COLOR_RGBA2RGB)
        # ファイルに出力
        out.write(img)
        # FPS
        print('fps: {0}'.format(1 / (time.time() - last_time)))

out.release()
cv2.destroyAllWindows()
