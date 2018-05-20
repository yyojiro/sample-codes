# -*- coding: utf-8 -*-
'''
キャプチャしたAVIファイルをシークする。
'''

import wx
import numpy as np
import cv2

ORG_FILE_NAME = "cap.avi"

# 元ビデオファイル読み込み
org = cv2.VideoCapture(ORG_FILE_NAME)

# ビデオファイルの準備
end_flag, first_frame = org.read()
height, width, channels = first_frame.shape
print "width: %d , height: %d" % (width, height)
frame_count = org.get(cv2.CAP_PROP_FRAME_COUNT) - 1
print frame_count

class ImagePanel(wx.Panel):

    def __init__(self, parent, size, ID = wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID, size = size)
        self.size = size
        bmp = wx.Bitmap(self.size[0], self.size[1])
        self.stbmp = wx.StaticBitmap(self, bitmap = bmp)

    def redraw(self, img):
        assert(img.ndim == 3)
        assert(img.dtype == np.uint8)
        assert(img.shape[0] == self.size[1] and img.shape[1] == self.size[0])
        buf = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # ダブルバッファリングで描画
        bmp = wx.Bitmap.FromBuffer(img.shape[1], img.shape[0], buf)
        cdc = wx.ClientDC(self.stbmp)
        bdc = wx.BufferedDC(cdc, bmp)
        cdc.DrawBitmap(bmp,0,0)

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title)
        # 部品作成
        self.CreateStatusBar()
        self.ip = ImagePanel(self, size = (width, height))
        self.slider_seek = wx.Slider(self, name = "seek",
                                          style=wx.SL_AUTOTICKS | wx.SL_LABELS,
                                          value=1, minValue=1, maxValue=frame_count)
        self.slider_seek.SetTick(2)
        self.slider_seek.SetTickFreq(2)
        self.slider_seek.Bind(wx.EVT_SLIDER, self.slideEvent)
        # 部品配置
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ip, border = 10, flag = wx.ALIGN_CENTER | wx.ALL)
        sizer.Add(self.slider_seek, border = 10, flag = wx.ALIGN_CENTER | wx.GROW)
        self.SetSizerAndFit(sizer)
        # 初期画像描画
        self.ip.redraw(first_frame)

    def slideEvent(self, event):
        val = event.GetEventObject().GetValue()
        org.set(cv2.CAP_PROP_POS_FRAMES, val)
        end_flag, video_frame = org.read()
        self.ip.redraw(video_frame)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, wx.ID_ANY, "video seek")
    frame.Show()
    app.MainLoop()
