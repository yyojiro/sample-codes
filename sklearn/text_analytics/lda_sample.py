# -*- coding: utf-8 -*-
"""
LDAで潜在トピック解析するサンプル。
"""
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import mglearn
import numpy as np

################################
# データ取得
# categories = ['alt.atheism',
#               'comp.graphics',
#               'comp.os.ms-windows.misc',
#               'comp.sys.ibm.pc.hardware',
#               'comp.sys.mac.hardware',
#               'comp.windows.x',
#               'misc.forsale',
#               'rec.autos',
#               'rec.motorcycles',
#               'rec.sport.baseball',
#               'rec.sport.hockey',
#               'sci.crypt',
#               'sci.electronics',
#               'sci.med',
#               'sci.space',
#               'soc.religion.christian',
#               'talk.politics.guns',
#               'talk.politics.mideast',
#               'talk.politics.misc',
#               'talk.religion.misc']

# とりあえず
categories = ['rec.sport.baseball', 'comp.sys.mac.hardware']

# ニュース記事取得
dataset = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

# トレーニング用、検証用のデータセット作成
train_data, test_data, train_target, test_target = train_test_split(
    dataset.data, dataset.target, test_size=0.2)

# データの中身確認
print dataset.target_names
print "train data size %i" % len(train_data)
print "test data size %i" % len(test_data)

# モデル組み立て
tfidf_vec = TfidfVectorizer(lowercase=True,
                            ngram_range=(1, 3),
                            max_df=0.1,
                            min_df=5)
lda = LatentDirichletAllocation(n_components=4,
                                max_iter=200,
                                learning_method="batch")
model = Pipeline(steps=[('vec', tfidf_vec),
                        ('lda', lda)])

# 学習
model.fit(dataset.data)

# モデル保存
joblib.dump(model, 'lda_model.pkl')

# テストデータでPerplexity計算
test_vec = model.named_steps['vec'].transform(test_data)
lda_perp = model.named_steps['lda'].perplexity(test_vec)
print "Perplexity %i" % lda_perp

# LDAのトピックごとの単語10件表示
sorting = np.argsort(model.named_steps['lda'].components_, axis=1)[:, ::-1]
feature_names = np.array(model.named_steps['vec'].get_feature_names())
mglearn.tools.print_topics(topics=range(2),
                           feature_names=feature_names,
                           sorting=sorting,
                           topics_per_chunk=2,
                           n_words=10)
