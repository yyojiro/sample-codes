# -*- coding: utf-8 -*-
'''
ドコモクラウドAPIを利用した発話理解のサンプル。
詳しくは公式サイト見ましょう。
https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=speech_understanding&p_name=api_usage_scenario
'''

import json
import requests

# APIKEYはドコモクラウドAPI利用者登録して、アリケーション登録するともらえる
api_key = None
with open("secret.txt", "r") as file:
    api_key = file.read()

API_URL = 'https://api.apigw.smt.docomo.ne.jp/sentenceUnderstanding/v1/task?APIKEY=%s' % api_key.strip()


def build_request_data(text):
    req = {
        "projectKey": "OSU",
        "appInfo": {
            "appKey": "test_app"
        },
        "clientVer": "1.0.0",
        "language": "ja",
        "userUtterance": {
            "utteranceText": text
        }
    }
    return req


def main():
    test_text = 'すもももももももものうち'
    req_data = json.dumps(build_request_data(test_text))
    response = requests.post(API_URL,
                             headers={'Content-Type': 'application/json;charset=UTF-8'},
                             data=req_data)
    print json.dumps(response.json(), ensure_ascii=False, indent=2).encode("utf-8")


if __name__ == '__main__':
    main()
