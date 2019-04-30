# stateful
# prints to console after receiving an http request

from flask import Flask, render_template
import requests
import sqlite3

DATABASE = 'node_3_state1.db'

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

def make_style_sheet(background_color, number_of_actuators):
    for actuator in number_of_actuators:
        css = open('static/node_3.css', "w")
        css.write(""".circle {
            height: 25px;
            width: 25px;\n""")
        css.write("""\t \t \t  background-color: """ + background_color + """;""")
        css.write("""
            border-radius: 50%;
            display: inline-block;
        }""")
        css.close()

def make_html(shape, number_of_actuators):
    for actuator in number_of_actuators:
        html = open('templates/node_3.html', "w")
        html.write("""<html>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='node_3.css') }}">
        <body>
            <div class=\"""" + shape + 
            """\"></div>
            The first database
        </body>
    </html>""")
        html.close()

@app.route('/', methods=['GET', 'POST'])
def node_3():
    # get for database queries
    # post for database updates
    number_of_actuators = 1
    with sqlite3.connect(DATABASE) as db:
        cur = db.cursor()
        cur.execute('SELECT * FROM current_state')
        state = ''
        for row in cur:
            state = row[0]
        if state == "1":
            cur.execute('UPDATE current_state SET state = false WHERE state = true')
            make_style_sheet("blue", number_of_actuators)
            # make_html("circle")
        else:
            cur.execute('UPDATE current_state SET state = true WHERE state = false')
            make_style_sheet("black", number_of_actuators)
            # make_html("square")

        cur.execute('SELECT * FROM current_state')
        for row in cur:
            state = row[0]
        
        return render_template('node_3.html')

if __name__ == '__main__':
    app.run()