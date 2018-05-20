#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
USBカメラで顔画像認識
'''

import cv2

ESC_KEY = 27   # Escキー
INTERVAL = 33  # msec
CASCADE_FILE = "haarcascade_frontalface_alt.xml"
MY_WINDOW_NAME = "window"
DEVICE_ID = 0


def main(device_id=0):
    # 分類器生成
    cascade = cv2.CascadeClassifier(CASCADE_FILE)

    # カメラ取得
    cap = cv2.VideoCapture(device_id)
    # 解像度を設定してみるが、デフォルトの640x480以上にならんこともある
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    camera_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print "(width,height) = (%d,%d)" % (camera_width, camera_height)
    print "fps: ", cap.get(cv2.CAP_PROP_FPS)
    print "auto focus: ", cap.get(cv2.CAP_PROP_AUTOFOCUS)

    # 初期フレームの読込
    end_flag, c_frame = cap.read()
    height, width, channels = c_frame.shape
    print "(width,height,channels) = (%d,%d,%d)" % (width, height, channels)

    # ウィンドウの準備
    cv2.namedWindow(MY_WINDOW_NAME)

    # 変換処理ループ
    while cap.isOpened():

        # 画像の取得と顔の検出
        img = c_frame
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))

        # 顔に枠をつける
        for (x, y, w, h) in face_list:
            color = (0, 0, 255)
            thickness = 3
            cv2.rectangle(c_frame, (x, y), (x + w, y + h), color, thickness=thickness)

        # 表示
        cv2.imshow(MY_WINDOW_NAME, c_frame)

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    main(DEVICE_ID)
