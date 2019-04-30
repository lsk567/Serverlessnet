from flask import Flask, request, render_template
import requests
import argparse
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hi, this switch is running.", 200

@app.route('/flip', methods=['POST'])
def flip():
    # Relayer url
    url = "172.17.0.1:4997/send"

    # Action params
    NAMESPACE = 'guest'
    ACTION = 'flip_switch'

    data = {"namespace" : NAMESPACE,
            "action"    : ACTION}

    response = requests.post(url, json=data)
    # print(response.text)
    
    return "Flip request sent.", 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=4999)