#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import voice_ctrl

app = Flask(__name__)
app.register_blueprint(voice_ctrl.app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()


