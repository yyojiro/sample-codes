# -*- coding: utf-8 -*-

"""
決定木のサンプル
"""

from sklearn.datasets import load_iris
from sklearn import tree

# みんな大好きirisデータ
iris = load_iris()

# 決定木を作って学習する
clf = tree.DecisionTreeClassifier(max_depth=3)
clf = clf.fit(iris.data, iris.target)

# テスト
predicted = clf.predict(iris.data)
print float(sum(predicted == iris.target)) / len(iris.target)

# 決定木を可視化
# Graphvizをインストールしておくこと
# https://www.graphviz.org/
import pydotplus as pdp
dot_data = tree.export_graphviz(clf,
                                out_file=None,
                                feature_names=iris.feature_names,
                                class_names=iris.target_names,
                                filled=True, rounded=True)
graph = pdp.graph_from_dot_data(dot_data)
graph.write_png("sample_tree.png")
