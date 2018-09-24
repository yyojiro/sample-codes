#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import os

batch_size = 128
num_classes = 10
epochs = 10
model_dir = './model'

# データ読み込み
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# ニューラルネットにぶち込むために成形
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# 答えのベクトル化
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# モデル作成
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

# 学習
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

# 保存
open(os.path.join(model_dir,'test_model.json'), 'w').write(model.to_json())
model.save_weights(os.path.join(model_dir, 'test_model_weights.hdf5'))

# 評価
score = model.evaluate(x_test, y_test, verbose=0)
classes = model.predict(x_test, batch_size=128)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print(classes)
