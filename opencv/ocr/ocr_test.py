# -*- coding: utf-8 -*-
'''
文字認識テスト用
あらかじめTesseractをインストールしておく必要がある。
'''

from PIL import Image
import sys
import pyocr
import pyocr.builders
import cv2

# Tesseractが入ってるか確認
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print(u"OCRがみつかりません")
    sys.exit(1)
tool = tools[0]
print(u"OCRツール名: %s" % (tool.get_name()))

# Tesseract用設定
builder = pyocr.builders.TextBuilder()
# なんかtesseract_flagsがデフォルトで['-psm', '3']ってなっててエラーになる。
# バグだと思うのでここで補正する。
print builder.tesseract_flags
builder.tesseract_flags = '--psm 3'.split()
builder.tesseract_configs = []

# 文字認識
txt = tool.image_to_string(Image.open("test1.png"),
                           lang="jpn",
                           builder=builder)
print(txt)

# 枠で囲ってみる
boxbuilder = pyocr.builders.WordBoxBuilder()
print boxbuilder.file_extensions
print boxbuilder.tesseract_flags
print boxbuilder.tesseract_configs

boxbuilder.tesseract_flags = '--psm 3'.split()
result = tool.image_to_string(Image.open("test1.png"),
                              lang="jpn",
                              builder=boxbuilder)

out = cv2.imread("test1.png")
for moji in result:
    cv2.rectangle(out, moji.position[0], moji.position[1], (0, 0, 255), 2)

cv2.imshow('image', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
