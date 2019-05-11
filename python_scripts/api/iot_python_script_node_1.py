from flask import Flask, request, render_template
import requests
import argparse
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/give_state', methods=['POST'])
def give_state():
    data = {}
    for key in request.form.keys():
        data[key] = request.form[key]

    temp = requests.post(url="http://172.17.0.1:4000/", data=data)
    return 200

@app.route('/get_state', methods=['GET'])
def get_state():
    result = requests.get(url='http://172.17.0.1:4000/state')
    return result.text

@app.route('/', methods=['POST'])
def node_1():
    # post data to OpenWhisk
    for key in request.form.keys():
        if "proxy" in key:
            requests.post(url=request.form[key])

    return "ok"

@app.route('/', methods=['GET'])
def node_1_get():
    # sends information back to webapp

    # gets all the port numbers
    out1 = subprocess.Popen(["docker", "ps"], stdout=subprocess.PIPE)
    out2 = subprocess.Popen(["egrep", "proxy*"], stdin=out1.stdout, stdout=subprocess.PIPE)
    out3 = subprocess.Popen(["sed", "-e", "s/[ ]\+/,/g"], stdin=out2.stdout, stdout=subprocess.PIPE)
    out4 = subprocess.Popen(["grep", "-o", "[^,]*,[^,]*$"], stdin=out3.stdout, stdout=subprocess.PIPE)
    out5 = subprocess.Popen(["grep", "-o", "^.*,"], stdin=out4.stdout, stdout=subprocess.PIPE)
    out6 = subprocess.Popen(["sed", "-e", "s/:/,/g"], stdin=out5.stdout, stdout=subprocess.PIPE)
    out7 = subprocess.Popen(["sed", "-e", "s/-/,/g"], stdin=out6.stdout, stdout=subprocess.PIPE)
    out8 = subprocess.Popen(["cut", "-d", ",", "-f", "2"], stdin=out7.stdout, stdout=subprocess.PIPE)
    out9 = subprocess.Popen(["xargs", "-n", "1"], stdin=out8.stdout, stdout=subprocess.PIPE)
    out10 = subprocess.Popen(["tr", "\n", ","], stdin=out9.stdout, stdout=subprocess.PIPE)
    anger, angererror = out10.communicate()
    port_numbers = anger.split(",")
    for port_number in port_numbers:
        if port_number == "":
            port_numbers.remove("")

    return json.dumps({'port_numbers': port_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4001')
