#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keras
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.datasets import mnist
import matplotlib.pyplot as plt

# 入力したものと同じっぽいものを出力するというネットワーク
# 中間層へらしたほうがいい結果が出るような気がする

# 定数
batch_size = 256
epochs = 5
model_dir = './model'

# データ読み込み
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# ニューラルネットにぶち込むために成形
# MINSTの画像は28*28の配列に0-254の数値の入ったデータ
x_train = x_train.reshape(60000, 28*28)
x_test = x_test.reshape(10000, 28*28)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

# エンコーダ
encoder = Sequential()
encoder.add(Dense(128, activation='relu', input_shape=(28*28,)))
# encoder.add(Dense(64, activation='relu'))

# デコーダ
decoder = Sequential()
# decoder.add(Dense(64, activation='relu'))
# decoder.add(Dense(128, activation='relu'))
decoder.add(Dense(28*28, activation='sigmoid'))

# オートエンコーダ
autoencoder = Sequential()
autoencoder.add(encoder)
autoencoder.add(decoder)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.fit(x_train, x_train,
                epochs=epochs,
                batch_size=batch_size,
                shuffle=True,
                validation_data=(x_test, x_test))

# テスト画像を変換
decoded_imgs = autoencoder.predict(x_test)

# 表示してみる
n = 10
plt.figure(figsize=(10, 4))
for i in range(n):
    # 入力画像を表示
    ax = plt.subplot(2, n, i+1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # 出力画像を表示
    ax = plt.subplot(2, n, i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()