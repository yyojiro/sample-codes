# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn import metrics

# みんな大好きirisデータ
iris = load_iris()
print iris.target_names

# クラスタ数
N_CLUSTERS = len(iris.target_names)

# クラスタリングする
cls = KMeans(n_clusters=N_CLUSTERS)
cls.fit(iris.data, iris.target)
km_pred = cls.predict(iris.data)

print iris.target
print km_pred
print metrics.accuracy_score(iris.target, km_pred)

# 各要素をラベルごとに色付けして表示する
for i in range(N_CLUSTERS):
    labels = iris.data[km_pred == i]
    plt.scatter(labels[:, 0], labels[:, 1])

# クラスタのセントロイド (重心) を描く
centers = cls.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], s=100,
            facecolors='none', edgecolors='black')
plt.show()
