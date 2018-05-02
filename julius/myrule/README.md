# Julius学習用

## 動作環境

* Raspberry PI 3 model B
* Linux raspberrypi 4.14.37-v7+
* juliusをALSA使う形式でインストールしていること
    * この辺参考にする　http://ezzep.blogspot.jp/2012/12/raspberry-pijulius.html

## 文法編集

まず文法の名前を決める。サンプルではmytestとしている。
.yomiファイルと.grammarファイルを編集する。

* 詳しくはここ　http://julius.osdn.jp/juliusbook/ja/desc_lm.html#id2537489

## ビルド

julius grammar-kitが必要。

```
$ git clone https://github.com/julius-speech/grammar-kit.git
$ ./build.sh mytest
```

## 起動

```
$ ./start.sh
```
