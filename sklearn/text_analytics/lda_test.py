# -*- coding: utf-8 -*-
"""
永続化したモデルをロードして使ってみる。
"""

from sklearn.externals import joblib
import numpy as np
import mglearn

# テストデータ(slashdotから拝借)
test = [
    'Serving as a consistent foundation for hybrid cloud environments, Red Hat Enterprise Linux 7.5 provides enhanced security and compliance controls, tools to reduce storage costs, and improved usability, as well as further integration with Microsoft Windows infrastructure both on-premise and in Microsoft Azure. ',
    'Analyst Salveen Richter and colleagues laid it out: "The potential to deliver one shot cures is one of the most attractive aspects of gene therapy, genetically engineered cell therapy, and gene editing. However, such treatments offer a very different outlook with regard to recurring revenue versus chronic therapies... While this proposition carries tremendous value for patients and society, it could represent a challenge for genome medicine developers looking for sustained cash flow." '
]

# モデル読み込み
model = joblib.load('lda_model.pkl')

# LDAのトピックごとの単語10件表示
sorting = np.argsort(model.named_steps['lda'].components_, axis=1)[:, ::-1]
feature_names = np.array(model.named_steps['vec'].get_feature_names())
mglearn.tools.print_topics(topics=range(2),
                           feature_names=feature_names,
                           sorting=sorting,
                           topics_per_chunk=2,
                           n_words=10)

# 計算結果
lda_test = model.transform(test)
print lda_test
