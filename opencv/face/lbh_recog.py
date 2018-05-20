#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
特定の顔画像を学習して判別する。
下記のインストールをしておかないとこける。
pip install opencv-contrib-python

"""

import cv2
import numpy as np

ESC_KEY = 27  # Escキー
MY_WINDOW_NAME = "window"
DEVICE_ID = 0

# Haar-like特徴分類器
cascadePath = "./haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascadePath)

# LBPH認識器
recognizer = cv2.face.LBPHFaceRecognizer_create()


def get_face_images(video_path):
    # 画像を格納する配列
    images = []

    # ビデオファイル読み込み
    video = cv2.VideoCapture(video_path)
    # ビデオファイルの準備
    end_flag, frame = video.read()

    while end_flag:
        # グレースケール変換
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Haar-like特徴分類器で顔を検知 (パラメータは適当)
        faces = cascade.detectMultiScale(img_gray, minSize=(100, 100))
        # 検出した顔画像の処理
        for (x, y, w, h) in faces:
            # 50x50にリサイズ
            roi = cv2.resize(img_gray[y: y + h, x: x + w], (50, 50), interpolation=cv2.INTER_LINEAR)
            # 画像を配列に格納
            images.append(roi)
        end_flag, frame = video.read()

    return images


def main():
    # 学習用ビデオファイル
    # 1つしかデータないや。
    # 判別器作るんだから、もっと他のデータもたくさん用意しないと。
    train_video = '../capture/cap.avi'
    label_id = 0
    images = get_face_images(train_video)
    labels = [label_id] * len(images)
    # トレーニング実施
    recognizer.train(images, np.array(labels))

    # カメラ取得
    device_id = 0
    cap = cv2.VideoCapture(device_id)

    # 変換処理ループ
    while cap.isOpened():
        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

        # 画像の取得と顔の検出
        img = c_frame
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))
        # 認識した顔に枠をつける
        for (x, y, w, h) in face_list:
            roi = cv2.resize(img_gray[y: y + h, x: x + w], (50, 50), interpolation=cv2.INTER_LINEAR)
            label, confidence = recognizer.predict(roi)
            # 予測結果をコンソール出力
            print("Label: {}, Confidence: {}".format(label, confidence))
            # 枠をつける
            color = (0, 0, 255)
            thickness = 3
            cv2.rectangle(c_frame, (x, y), (x + w, y + h), color, thickness=thickness)

        # 表示
        cv2.imshow(MY_WINDOW_NAME, c_frame)

        # Escキーで終了
        key = cv2.waitKey(33)
        if key == ESC_KEY:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
