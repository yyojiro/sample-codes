#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import audioop
from collections import deque
import os
import requests
import time
import math
import json
import subprocess

# APIKEYはGoogle Developer Platformに登録してもらってくる
api_key = None
with open("secret.txt", "r") as file:
    api_key = file.read()

# APIv2を使う
API_URL = 'https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&lang=ja-JP&maxresults=10&pfilter=0&xjerr=1&key=%s' % api_key.strip()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
THRESHOLD = 2500
SILENCE_LIMIT = 1
PREV_AUDIO = 0.5

def audio_int(num_samples=50):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
              for x in range(num_samples)]
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print "audio input mean %i " % r
    stream.close()
    p.terminate()
    return r


def listen_for_speech(threshold=THRESHOLD, num_phrases=1):
    """
    マイクからの音声を録音し、Google Speech APIに投げる。
    無音区域は取り除く。音は無音区域で区切られフレーズ数としてカウントする。
    :param threshold: 無音判定する閾値
    :param num_phrases: フレーズ数
    :return:
    """

    # マイク準備
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print "* Listening mic. "
    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    prev_audio = deque(maxlen=PREV_AUDIO * rel)
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if(sum([x > threshold for x in slid_win]) > 0):
            if(not started):
                print "Starting record of phrase"
                started = True
            audio2send.append(cur_data)
        elif started:
            print "Finished"
            # The limit was reached, finish capture and deliver.
            filename = save_speech(list(prev_audio) + audio2send, p)
            # Send file to Google and get response
            r = stt_google(filename)
            if num_phrases == -1:
                print r
            else:
                response.append(r)
            # Remove temp file. Comment line to review.
            #os.remove(filename)
            # Reset all
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            prev_audio = deque(maxlen=0.5 * rel)
            audio2send = []
            n -= 1
            print "Listening ..."
        else:
            prev_audio.append(cur_data)

    print "* Done recording"
    stream.close()
    p.terminate()

    return response


def save_speech(data, p):
    """ Saves mic data to temporary WAV file. Returns filename of saved
        file """

    # filename = 'output_'+str(int(time.time()))
    filename = 'output'
    # writes data to WAV file
    data = ''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    conv_cmd = "sox %s.wav %s.flac rate 16k" % (filename, filename)
    print subprocess.check_output(conv_cmd.split())
    return filename + '.flac'


def stt_google(audio_file):
    """
    GoogleSpeechAPIに送る
    :param audio_file:
    :return:
    """

    del_flac = False

    with open(audio_file, "rb") as file:
        audio_data = file.read()

    response = None
    # 音声ファイルはサンプリングレート16000のflac形式じゃないとダメ。
    headers = {'Content-type': 'audio/x-flac; rate=16000'}
    try:
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
    except:
        print "Couldn't parse service response"
        response = None

    if del_flac:
        os.remove(audio_file)  # Remove temp file

    return response


if __name__ == '__main__':
    # 背景ノイズの平均を取得
    audio_int()
    # 聞き取り開始
    data = listen_for_speech()
    try:
        print data[0][0]['utterance']
    except:
        print "No input recieved."
