from flask import Flask
import requests
import sqlite3
import json

DATABASE = 'actuator_states.db'

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def accessor():
    # get for database queries (ui)
    with sqlite3.connect(DATABASE) as db:
        cur = db.cursor()
        cur.execute('SELECT * FROM current_states')
        states = {}
        for row in cur:
            states[row[0]] = row[1]
    return json.dumps({'actuator_states': states})
    
@app.route('/', methods=['POST'])
def updater():
    # post for database updates (used by ui api)
    with sqlite3.connect(DATABASE) as db:
        cur = db.cursor()
        for key in request.form.keys():
            if cur.execute('SELECT EXISTS(SELECT * FROM current_states WHERE actuator = ' + key + ')') == 1:
                cur.execute('UPDATE current_states SET state = ' + request.form[key] + ' WHERE actuator = ' + key)
            else:
                cur.execute('INSERT INTO current_states VALUES (' + key + ', ' + request.form[key] + ')')
    
    data = accessor()
    # my machine
    temp = requests.post(url="http://160.39.130.33:5000", json=data)
    return "ok"

if __name__=="__main__":
    app.run(host='0.0.0.0')