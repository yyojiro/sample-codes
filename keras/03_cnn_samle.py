#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Activation, BatchNormalization, Flatten
from keras.datasets import mnist
import os

# CNNで画像認識するサンプル
# CNNの説明は下記サイトが丁寧でわかりやすい。
# https://postd.cc/how-do-convolutional-neural-networks-work/
# https://deepage.net/deep_learning/2016/11/07/convolutional_neural_network.html

batch_size = 256
num_classes = 10
epochs = 5
img_width = 28
img_height = 28
model_dir = './model'

# いつものMNIST画像読み込み
# データ読み込み
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(60000, img_width, img_height, 1)
x_test = x_test.reshape(10000, img_width, img_height, 1)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# 答えのベクトル化(one-hotにする)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# CNNモデル作成
# Convolution、Pooling、Convolution、Pooling・・・と繰り返して、最後にFlattenする
# 特徴数の少ない荒い識別からスタートして、徐々に精細なフィルタになるように組たてる
input_shape = [img_height, img_width, 1]
model = Sequential()

model.add(Conv2D(16, (5, 5), padding='same', input_shape=input_shape))
model.add(BatchNormalization())  # Convolutionの後に入れると収束が早くなるという噂
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# 最終的な識別はFully Connectedで行うのでFlattenする
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# コンパイル
# ここのパラメータいじりでいろいろ変わるけど、何がベストかはよくわからん
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 学習
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

# 保存
open(os.path.join(model_dir, 'test_model.json'), 'w').write(model.to_json())
model.save_weights(os.path.join(model_dir, 'test_model_weights.hdf5'))

# 評価
score = model.evaluate(x_test, y_test, verbose=0)
classes = model.predict(x_test, batch_size=128)
print('Test loss:', score[0])  # Test loss: 0.047747481274517486
print('Test accuracy:', score[1])  # Test accuracy: 0.9836
print(classes)
