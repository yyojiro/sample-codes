# -*- coding: utf-8 -*-

"""
TF-IDFのサンプル。
文字列が何語かを判定する。
元ネタはscikit-learnのチュートリアルだったが、原型まったくなし。
テストデータは下記のスクリプト使って拾ってくる。
https://github.com/scikit-learn/scikit-learn/blob/master/doc/tutorial/text_analytics/data/languages/fetch_data.py
"""

from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

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
# 日本語とかを扱う場合はtokenizerを設定してやる。
# 参考 https://qiita.com/asatohan/items/7a247eb533a5adba9e87
clf = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', MultinomialNB())])

# データセットを「トレーニング用」と「テスト用」に分割。
# cross validationとかに使う場合に便利。
# 参考　http://docs.pyq.jp/python/machine_learning/tips/train_test_split.html
# train_data   トレーニング用データ
# test_data    テスト用データ
# train_target トレーニング用ラベル（答え）
# test_target  テスト用ラベル
train_data, test_data, train_target, test_target = train_test_split(
    dataset.data, dataset.target, test_size=0.01)

# ここで機械学習。
# 学習結果の評価する予定がなければ、dataset.data, dataset.target使えばいい。
# clf.fit(dataset.data, dataset.target)
clf.fit(train_data, train_target)

# 実験
test_str = "This is a pen."
predicted = clf.predict([test_str])
print('"%s" is "%s"' % (test_str, dataset.target_names[predicted[0]]))


##################################################
# 以下は学習結果を評価するためのコード
from sklearn import metrics
y_predicted = clf.predict(test_data)
print(metrics.classification_report(test_target, y_predicted,
                                    target_names=dataset.target_names))
