#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
juliusから受け取った結果で何かする。

juliusからこんな感じのxmlが来る。
<RECOGOUT>
  <SHYPO RANK="1" SCORE="-1959.033691" GRAM="0">
    <WHYPO WORD="[s]" CLASSID="6" PHONE="silB" CM="1.000"/>
    <WHYPO WORD="今" CLASSID="4" PHONE="i m a" CM="1.000"/>
    <WHYPO WORD="何時" CLASSID="5" PHONE="n a N j i" CM="0.997"/>
    <WHYPO WORD="[s]" CLASSID="7" PHONE="silE" CM="1.000"/>
  </SHYPO>
</RECOGOUT>

"""

import socket
from xml.etree.ElementTree import *
import subprocess
import datetime

host = '127.0.0.1'
port = 10500


def say(message):
    """
    別に関数にしなくてもよかったんだけどよく使うから。
    :param message:
    :return:
    """
    subprocess.call(['say', message])


def say_time():
    """
    現在日時を喋らせるだけ
    :return:
    """
    date = datetime.datetime.now()
    say('"%i時%i分です"' % (date.hour, date.minute))


def process(elem):
    """
    ここでいろいろ処理する。
    もうちょっと真面目にデータ構造を考えたほうがいい。
    構文解釈してデータ作ってタスク処理するとか。
    :param elem: juliusから来たRECOGOUTタグの中身
    :return:
    """
    continue_flag = 0
    for whypo in elem.findall('./SHYPO/WHYPO'):
        word = whypo.get('WORD')
        cm = float(whypo.get('CM'))
        if cm < 0.9:
            # 認識率悪い時は無視
            say(u'なんかいった？')
            return
        if word == u'ハロー':
            continue_flag = 1
        if word == u'ナビ' and continue_flag == 1:
            say(u'ハロー！')
        if word == u'今':
            continue_flag = 2
        if word == u'何時' and continue_flag == 2:
            say_time()


def main():
    # juliusはデフォルトtcp:10500で待っている
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    say(u'起動します')
    try:
        data = ''
        while 1:
            # RECOGOUTタグが認識した結果を意味する
            if '</RECOGOUT>\n.' in data:
                print data
                # \n.が区切りになっているので、splitで切って必要な分にする
                elem = fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].split('\n.')[0])
                process(elem)
                # リセット
                data = ''
            else:
                data += str(client.recv(1024))
                print('wait')
    except KeyboardInterrupt:
        client.close()


if __name__ == "__main__":
    main()
