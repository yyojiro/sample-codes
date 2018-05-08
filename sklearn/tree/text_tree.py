# -*- coding: utf-8 -*-

"""
日本語の文章を解析して、適切な回答を出す。
形態素解析にはjanomeを使う。
"""
from sklearn.pipeline import Pipeline
from sklearn import tree
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from janome.tokenizer import Tokenizer
#from sklearn.ensemble import RandomForestClassifier


def my_tokenizer(text):
    text = text.replace('"','')
    t = Tokenizer()
    tokens = t.tokenize(text)
    return [token.surface for token in tokens]


# 学習データ読み込み
data = ''
with open("test.csv", "rb") as file:
    data = np.loadtxt(file, delimiter=',',
                      dtype='U100',
                      converters={1: lambda s: s.decode('utf8')})

# ラベルを取り出す
train_target = data[:, 0:1].ravel()
# 学習用データ
train_data = data[:, 1:].ravel()

# テキストをベクトル化する
vectorizer = TfidfVectorizer(ngram_range=(1, 2),
                             use_idf=False,
                             tokenizer = my_tokenizer)
# 決定木
clf = tree.DecisionTreeClassifier(max_depth=4,
                                  random_state=1)

# 処理のパイプライン
pipeline = Pipeline([('vect', vectorizer),
                     ('clf', clf)])
# 学習
pipeline.fit(train_data, train_target)

# 実験
predicted = pipeline.predict([u'テレビつけてちょ',
                              u'テレビけして',
                              u'さいなら'])
print predicted

# 正答率
predicted = pipeline.predict(train_data)
print float(sum(predicted == train_target)) / len(train_target)

# 決定木を可視化
# Graphvizをインストールしておくこと
# https://www.graphviz.org/
# 日本語を扱うためには下記ファイル
# "C:\Python27\lib\site-packages\sklearn\tree\export.py"
# を編集しfontname=となっているところで日本語フォント名に変えておくこと。

import pydotplus as pdp
# python3使っておけばよかった。utf-8変換だるい。
feature_names = map(lambda x: x.encode('utf-8'), pipeline.named_steps['vect'].get_feature_names())
class_names = map(lambda x: x.encode('utf-8'), pipeline.named_steps['clf'].classes_)
dot_data = tree.export_graphviz(clf,
                                out_file=None,
                                feature_names=feature_names,
                                class_names=class_names,
                                filled=True, rounded=True,
                                special_characters=True)
graph = pdp.graph_from_dot_data(dot_data)
graph.write_png("sample_tree.png")
