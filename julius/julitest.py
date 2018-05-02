#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
juliusからメッセージを受け取って表示するだけのサンプル
"""

import socket

host = '127.0.0.1'
port = 10500


def main():
    # juliusはデフォルトtcp:10500で待っている
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        data = ''
        while 1:
            if '</RECOGOUT>\n.' in data:
                print data
                data = ''
            else:
                data += str(client.recv(1024))
                print('wait') # no recoginzed word
    except KeyboardInterrupt:
        client.close()


if __name__ == "__main__":
    main()
