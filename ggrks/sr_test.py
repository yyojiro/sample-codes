#!/usr/bin/env python
# -*- coding: utf-8 -*-

import speech_recognition as sr

"""
SpeechRecognitionパッケージを使うテスト
"""

api_key = None
with open("secret.txt", "r") as file:
    api_key = file.read()

r = sr.Recognizer()
with sr.Microphone(device_index=2, sample_rate=48000, chunk_size=1024) as source:
#with sr.Microphone() as source:
    print("start")
    audio = r.listen(source)

try:
    print(r.recognize_google(audio,
                             language='ja-JP',
                             key=api_key))
except LookupError:
    print("失敗")
