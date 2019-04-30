from flask import Flask, request, render_template
import requests
import argparse
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def node_1():
    # post data to OpenWhisk
    for key in request.form.keys():
        if "docker" in key:
            requests.post(url=request.form[key])

    return "ok"

@app.route('/', methods=['GET'])
def node_1_get():
    # sends information back to webapp

    # gets all the port numbers
    out1 = subprocess.Popen(["docker", "ps"], stdout=subprocess.PIPE)
    out2 = subprocess.Popen(["egrep", "docker*"], stdin=out1.stdout, stdout=subprocess.PIPE)
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
    app.run(host='0.0.0.0')