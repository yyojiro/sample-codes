#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from keras.models import model_from_json
from keras.datasets import mnist
import matplotlib.pyplot as plt

# テストデータ読み込み
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 成形
x_test = x_test.reshape(10000, 28*28)
x_test = x_test.astype('float32')
x_test /= 255

# モデルの読み込み
model = model_from_json(open('model/test_model.json', 'r').read())

# 重みの読み込み
model.load_weights('model/test_model_weights.hdf5')

# テストに使うやつを適当に決める
test_index = np.random.randint(1000)

# 予測結果
y = model.predict(x_test[test_index].reshape(1, 28*28))
print("predicted: " + str(np.argmax(y)))
print("answer: " + str(y_test[test_index]))

# テスト画像の表示
plt.imshow(x_test[test_index].reshape(28, 28))
plt.show()
