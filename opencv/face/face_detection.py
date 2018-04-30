# -*- coding: utf-8 -*-
'''
顔画像認識テスト用
'''

import wx
import numpy as np
import cv2
import sys
from PIL import Image

# データは下記から取得
# https://github.com/opencv/opencv/blob/master/data/haarcascades/
# https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/cascades/
cascade_path = "./haarcascade_frontalface_alt.xml"

# カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

# 使う画像
file_path = 'lena.png'
overlay_img_path = "pop.png"


class ImagePanel(wx.Panel):
    def __init__(self, parent, size, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID, size=size)
        self.size = size
        bmp = wx.Bitmap(self.size[0], self.size[1])
        self.stbmp = wx.StaticBitmap(self, bitmap=bmp)

    def redraw(self, img):
        buf = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bmp = wx.Bitmap.FromBuffer(img.shape[1], img.shape[0], buf)
        self.stbmp.SetBitmap(bmp)


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title)
        # 部品作成
        self.CreateStatusBar()
        self.target_img = cv2.imread(file_path)
        self.ip = ImagePanel(self, size=(self.target_img.shape[1], self.target_img.shape[0]))
        self.change_button = wx.Button(self, label=u"顔認識", size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.btnHandler, self.change_button)

        # 配置
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ip, border=10, flag=wx.ALIGN_CENTER | wx.ALL)
        sizer.Add(self.change_button, flag=wx.ALIGN_CENTER )
        self.SetSizerAndFit(sizer)
        # ファイル名をステータスバーに表示
        self.SetStatusText(file_path)
        # 初期画像描画
        self.ip.redraw(self.target_img)

    def btnHandler(self, event):
        if self.change_button.GetLabel() == u"顔認識":
            self.change_button.SetLabel(u"戻す")
            self.imgProcessing()
        else:
            self.change_button.SetLabel(u"顔認識")
            self.ip.redraw(self.target_img)

    def imgProcessing(self):
        # 顔検出
        img = cv2.imread(file_path)
        over_img = cv2.imread(overlay_img_path,
                               cv2.IMREAD_UNCHANGED)
        facerect = cascade.detectMultiScale(img,
                                            scaleFactor=1.1,
                                            minNeighbors=2,
                                            minSize=(10, 10))
        for rect in facerect:
            x1 = rect[0]
            y1 = rect[1]
            x2 = rect[0] + rect[2]
            y2 = rect[1] + rect[3]
            resized_ol_image = resize_image(over_img,
                                            rect[2],
                                            rect[3])
            img = overlayOnPart(img, resized_ol_image, rect[0], rect[1])
        self.ip.redraw(img)


def resize_image(image, height, width):
    # 元々のサイズを取得
    org_height, org_width = image.shape[:2]
    # 大きい方のサイズに合わせて縮小
    if float(height) / org_height > float(width) / org_width:
        ratio = float(height) / org_height
    else:
        ratio = float(width) / org_width
    # リサイズ
    resized = cv2.resize(image, (int(org_height * ratio), int(org_width * ratio)))
    return resized


def overlayOnPart(src_image, overlay_image, posX, posY):
    # オーバレイ画像のサイズを取得
    ol_height, ol_width = overlay_image.shape[:2]
    # OpenCVの画像データをPILに変換
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
    src_image_PIL = Image.fromarray(src_image_RGBA)
    overlay_image_PIL = Image.fromarray(overlay_image_RGBA)
    # 合成のため、RGBAモードに変更
    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')
    # 同じ大きさの透過キャンパスを用意
    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255, 255, 0))
    # 用意したキャンパスに上書き
    tmp.paste(overlay_image_PIL, (posX, posY), overlay_image_PIL)
    # オリジナルとキャンパスを合成して保存
    result = Image.alpha_composite(src_image_PIL, tmp)
    return cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, wx.ID_ANY, sys.argv[0])
    frame.Show()
    app.MainLoop()
