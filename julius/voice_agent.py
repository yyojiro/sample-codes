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
import time
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler('/var/log/vagent.log', when="s", interval=1, backupCount=3)
handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
logger.addHandler(handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
logger.addHandler(console_handler)
logger.debug('start')

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
    考えるの面倒だから機械学習でも使うか。
    :param elem: juliusから来たRECOGOUTタグの中身
    :return:
    """
    score = 1.0
    threshold = 0.5  # この閾値を下回ると無視する
    sentence = ''
    for whypo in elem.findall('./SHYPO/WHYPO'):
        word = whypo.get('WORD')
        cm = float(whypo.get('CM'))
        score *= cm
        sentence += word

    if score < threshold:
        # リーザというのはうちの嫁が適当に名付けたエージェント名。
        if u'リーザ' in sentence: 
            # 認識率が悪い時
            say(u'なんかいった？')
        return

    logger.info("score %f" % score)
    if u'ハローリーザ' in sentence:
        say(u'ハロー！')
    if u'今何時' in sentence:
        say_time()
    if u'テレビ' in sentence:
        if u'つけて' in sentence:
            subprocess.call('irsend SEND_ONCE sharptv key_power'.split())
            say(u'テレビをつけます')
        if u'消して' in sentence:
            subprocess.call('irsend SEND_ONCE sharptv key_power'.split())
            say(u'テレビを消します')
    if u'音量' in sentence:
        if u'上げて' in sentence:
            subprocess.call('irsend SEND_ONCE sharptv volume_up'.split())
            say(u'音量上げます')
        if u'下げて' in sentence:
            subprocess.call('irsend SEND_ONCE sharptv volume_down'.split())
            say(u'音量下げます')
    if u'IP教えて' in sentence:
        ipaddr = subprocess.check_output("ifconfig wlan0 | grep 'inet ' | awk '{print $2}'", shell=True)
        say(u'%sです' % ipaddr)


def wait_for_message(client):
    data = ''
    while True:
        # RECOGOUTタグが認識した結果を意味する
        try:
            if '</RECOGOUT>\n.' in data:
                logger.info(data)
                # \n.が区切りになっているので、splitで切って必要な分にする
                elem = fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].split('\n.')[0])
                # 処理する
                process(elem)
                # リセット
                data = ''
            else:
                byte_data = client.recv(1024)
                if byte_data == '':
                    # 相手が切れるとrecvから0byteが返ってくるので、ここで例外にする
                    raise socket.error()
                data += str(byte_data)
                logger.debug('wait')
        except ParseError:
            logger.error(ParseError)


def connect_julius():
    # juliusはデフォルトtcp:10500で待っている
    host = '127.0.0.1'
    port = 10500
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            say(u'音声認識できます')
            return client
        except socket.error:
            logger.error("can not get connection. try reconnect.")
            time.sleep(3)


def main():
    say(u'起動します')
    client = connect_julius()
    while True:
        try:
            wait_for_message(client)
        except socket.error:
            say(u'音声認識がきれました')
            logger.warning("server socket closed. try reconnect.")
            client = connect_julius()
        except KeyboardInterrupt:
            client.close()
            return


if __name__ == "__main__":
    main()
