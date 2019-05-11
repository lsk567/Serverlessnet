from flask import Flask, request, render_template
import requests
import argparse
import subprocess
import json
import os
import sys

app = Flask(__name__)

if len(sys.argv) != 2:
    raise Exception('Invalid number of command line arguments. 1 expected, but ' + str(len(sys.argv) - 1) + ' given.')

target = int(sys.argv[1])
relayerPort = 4997

@app.route('/', methods=['GET'])
def hello():
    return 'Hi, this switch is running.', 200

@app.route('/flip', methods=['POST'])
def flip():
    # Relayer url
    url = 'http://172.17.0.1:' + str(relayerPort) + '/send'

    # Action params
    NAMESPACE = 'guest'
    ACTION = 'flip_switch'

    data = {'namespace' : NAMESPACE,
            'action'    : ACTION,
            'target'    : target}

    response = requests.post(url, json=data)
    
    return 'Flip request sent to port ' + str(target), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
