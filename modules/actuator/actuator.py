"""
The actuator module is used to the state of an actuator.

Author: Jessica Huynh, Jerry Lin
"""

from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hi, the actuator is running.", 200

@app.route('/state', methods=['GET'])
def get_state():
    # Status check
    file = open("state.txt", "r")
    state = file.read()

    return "The actuator state is " + state, 200

@app.route('/state', methods=['POST'])
def toggle_state():
    # read state
    file = open("state.txt", "r")
    state = file.read()
    # flip state
    state = str(int(not bool(int(state))))
    # write to file
    file2 = open("state.txt", "w")
    file2.write(state)
    # return status
    return jsonify({
        "state": state
    }), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)