#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
いろいろ作りかけ
apache経由でしゃべらす場合は
# usermod -G audio www-data
が必要。
"""

from flask import Blueprint, render_template, jsonify, request, make_response
import subprocess

app = Blueprint('voice_ctrl', __name__)

@app.route("/voice_ctrl", methods=['GET'])
def top():
    return render_template('voice_ctrl.html', p={})

VOICE = '/usr/share/hts-voice/htsvoice-tohoku-f01/tohoku-f01-neutral.htsvoice'
DICTIONARY = '/var/lib/mecab/dic/open-jtalk/naist-jdic/'

@app.route("/voice_ctrl", methods=['POST'])
def test_run():
    req_obj = request.json
    message = u'%s' % req_obj['message']
    command = u'echo "%s" |' \
              ' open_jtalk -x %s -m %s -s %s -p %s -a %s -b %s -r %s -fm %s -u %s -jm %s -jf %s -ow /dev/stdout |' \
              ' aplay --quiet' \
              % (message,
                 DICTIONARY,
                 VOICE,
                 req_obj['param_s'],
                 req_obj['param_p'],
                 req_obj['param_a'],
                 req_obj['param_b'],
                 req_obj['param_r'],
                 req_obj['param_fm'],
                 req_obj['param_u'],
                 req_obj['param_jm'],
                 req_obj['param_jf'],
                 )

    #print command.encode('utf-8')
    subprocess.call(command.encode('utf-8'), shell=True)
    return make_response(jsonify({'result': command.encode('utf-8')}))