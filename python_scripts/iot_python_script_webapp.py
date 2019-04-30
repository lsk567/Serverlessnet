from flask import Flask, render_template, request
import requests, argparse
from time import sleep
import json
import os
import fileinput

app = Flask(__name__)
data = {}

@app.route('/', methods=['GET'])
def node_1_get():
    # gets port numbers and cleans them up
    temp = requests.get(url="http://128.59.22.210:4001/").json()
    port_numbers = temp["port_numbers"]
    cleaned_port_numbers = []
    for port_number in port_numbers:
        if port_number != '':
            cleaned_port_numbers.append(port_number)
    
    html = None
    if os.stat('templates/node_1.html').st_size == 0:
        html = open('templates/node_1.html', "w+")
    else:
        html = open('templates/node_1.html', "w")

    html.write("""<html>
    <body>
        <head>
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js"></script>
          <link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">
          <script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>
        </head>\n""")
    for port in cleaned_port_numbers:
        html.write("""        <div><input type="checkbox" class='toggle' id='box""" + port + """' checked data-toggle="toggle"></div>\n""")
        html.write("""        <div class='status' id='toggledbox""" + port + """'>On</div>\n""")
    html.write("""    </body>
    <script>
    $(document).ready(function() {\n""")
    for port in cleaned_port_numbers:
        html.write("""        var port""" + port + """ = 'On'\n""")
    for port in cleaned_port_numbers:
        html.write("""        $('#box""" + port + """').change(function() {
          var status = document.getElementById('toggledbox""" + port + """').innerHTML
          if (status == 'On') {
            $('#toggledbox""" + port + """').html('Off');
          }
          else {
            $('#toggledbox""" + port + """').html('On');
            $.ajax({
              url: "/get_toggled_status",
              type: "get",
              data: {status: port"""+ port + """, port: """ + port + """},
              success: function(response) {
                $('#toggledbox""" + port + """').html('response');
              }
            });
          }
        });\n""")
    html.write("""      });
    </script>
</html>""")
    html.close()

    # arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, dest='url')
    args = parser.parse_args()

    # parse data with commas
    url_list = args.url.split(",")
    i = 0
    for port in cleaned_port_numbers:
        open_whisk_var = "open_whisk" + str(port)
        data[open_whisk_var] = url_list[i]
        i += 1

    make_style_sheet("blue", 1)

    return render_template('node_1.html')

@app.route('/', methods=['POST'])
def node_1_post():
    for key in request.form.keys():
        if request.form[key] == '0':
            change_style_sheet("blue", "black", 1)
        else:
            change_style_sheet("black", "blue", 1)
    return render_template('node_1.html')

# check which one sent the toggled status
@app.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')
    port_number = request.args.get('port')

    if current_status == 'On':
        sending_data = data["open_whisk" + str(port_number)]
        # container
        connected = False
        # need to check which URLs are open
        while not connected:
            result = requests.post(url="http://128.59.22.210:4001/", json=sending_data)
            sleep(1)
            if result.status_code == requests.codes.ok:
                connected = True

    return render_template('node_1.html')

def make_style_sheet(background_color, number_of_actuators):
    for actuator in number_of_actuators:
        css = open('static/node_1.css', "w")
        css.write(""".circle {
            height: 25px;
            width: 25px;\n""")
        css.write("""\t \t \t  background-color: """ + background_color + """;""")
        css.write("""
            border-radius: 50%;
            display: inline-block;
        }""")
        css.close()

def change_style_sheet(previous_color, new_color, number_of_actuators):
    with fileinput.FileInput('static/node_1.css', inplace=True, backup='.bak') as css:
        for line in css:
            line.replace(previous_color, new_color)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
