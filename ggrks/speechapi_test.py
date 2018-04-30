#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Google Speech APIを使う実験。
pythonだったら素直にSDK使えと言われそう。
Cloud Speech APIではないので要注意。
'''

import json
import requests

# APIKEYはGoogle Developer Platformに登録してもらってくる
api_key = None
with open("secret.txt", "r") as file:
    api_key = file.read()

# APIv2を使う
API_URL = 'https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&lang=ja-JP&maxresults=10&pfilter=0&xjerr=1&key=%s' % api_key.strip()

# 音声ファイルはサンプリングレート16000のflac形式じゃないとダメ。
headers = {'Content-type': 'audio/x-flac; rate=16000'}
audio_file = "test.flac"


def main():
    with open(audio_file, "rb") as file:
        audio_data = file.read()
    response = requests.post(API_URL,
                             headers=headers,
                             data=audio_data)
    # なんか結果のJSONが複数行になる
    for result in response.text.split('\n'):
        obj = None
        try:
            obj = json.loads(result)
        except:
            print result
            continue
        print json.dumps(obj,
                         ensure_ascii=False,
                         indent=2).encode("utf-8")


if __name__ == '__main__':
    main()
