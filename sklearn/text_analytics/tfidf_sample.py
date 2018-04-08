# -*- coding: utf-8 -*-

"""
TF-IDFのサンプル。
元ネタは下記のチュートリアルだったが、原型まったくなし。
https://github.com/scikit-learn/scikit-learn/blob/master/doc/tutorial/text_analytics/skeletons/exercise_01_language_train_model.py
"""

from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# データ読み込み。
# load_files関数は以下のディレクトリ・ファイル構成で学習用の元データを作ってくれる。
# （ラベル）/（学習データファイルたち）
# dataset.target: ラベル
# dataset.data: 学習用生データ
languages_data_folder = "./paragraphs"
dataset = load_files(languages_data_folder)


# ベクトル化 -> TF-IDF変換 -> クラス分類器のパイプライン
# 最初からこれ作っとけやというもの。
# CountVectorizerはデフォルトでは文字列をスペース区切りでベクトル化している。
# TfidfVectorizerを使えば、ベクトル化 -> TF-IDF変換を1発でやってくれる。
# 日本語とかを扱う場合はtokenizerを設定する。
# 参考 https://qiita.com/asatohan/items/7a247eb533a5adba9e87
# 分類器は種類もいろいろパラメータもいろいろ。
# clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 3))),
#                 ('tfidf', TfidfTransformer(use_idf=False)),
#                 ('clf', LinearSVC())])
vectorizer = TfidfVectorizer(ngram_range=(1, 3),
                             use_idf=False)
clf = Pipeline([('vect', vectorizer),
                ('clf', LinearSVC())])

# データセットを「トレーニング用」と「テスト用」に分割
# 参考　http://docs.pyq.jp/python/machine_learning/tips/train_test_split.html
# train_data   トレーニング用データ
# test_data    テスト用データ
# train_target トレーニング用ラベル（答え）
# test_target  テスト用ラベル
train_data, test_data, train_target, test_target = train_test_split(
    dataset.data, dataset.target, test_size=0.1)

# ここで機械学習
# clf.fit(dataset.data, dataset.target)
clf.fit(train_data, train_target)

# ここでテスト
y_predicted = clf.predict(test_data)

test_str = "This is a pen."
predicted = clf.predict([test_str])
print('"%s" is "%s"' % (test_str, dataset.target_names[predicted[0]]))


##################################################
# 以下は学習結果を評価するためのコード
from sklearn import metrics
print(metrics.classification_report(test_target, y_predicted,
                                    target_names=dataset.target_names))


##################################################
# 分類器たちを比較する
# デフォルト設定でどこまでの成績を出せるのか
# from sklearn.naive_bayes import *
# from sklearn.ensemble import *
# from sklearn.linear_model import *
# from sklearn.model_selection import cross_val_score
#
# print "おまけ　分類器の比較"
# clf_names = ["LinearSVC",
#              "Perceptron",
#              "MultinomialNB",
#              "ExtraTreesClassifier",
#              "RandomForestClassifier"]
# for clf_name in clf_names:
#     clf = Pipeline([('vect', vectorizer),
#                     ('clf', eval("%s()" % clf_name))])
#     scores = cross_val_score(clf, dataset.data, dataset.target, cv=5)
#     score = sum(scores) / len(scores)  # モデルの正解率を計測
#     print "%s: %s" % (clf_name, score)
