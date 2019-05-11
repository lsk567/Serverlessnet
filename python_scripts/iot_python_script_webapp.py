from flask import Flask, render_template, request, redirect, url_for
import requests, argparse
from time import sleep
import json
import os
import fileinput

app = Flask(__name__)
data = {}
cleaned_port_numbers = ['4000']

@app.route('/', methods=['GET'])
def node_1_get():
    # gets port numbers and cleans them up
    # temp = requests.get(url="http://128.59.22.210:4000/").json()
    # port_numbers = temp["port_numbers"]
    # cleaned_port_numbers = []
    # for port_number in port_numbers:
    #     if port_number != '':
    #         cleaned_port_numbers.append(port_number)
    
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
          <link rel="stylesheet" href="../static/node_1.css">
        </head>\n""")
    for port in cleaned_port_numbers:
        html.write("""        <div><input type="checkbox" class='toggle' id='box""" + port + """' checked data-toggle="toggle"></div>\n""")
        html.write("""        <div class='status' id='toggledbox""" + port + """'>On</div>\n""")
    html.write("""    <div class="blue", id="circle0"></div>
    </body>
    <script>
    $(document).ready(function() {
        var interval = 1000; 
        function get_status() {
            $.ajax({
            type: "GET",
            url: "http://localhost:5000/access",
            success: function(response) {
                console.log(response);
                response = JSON.parse(response);
                console.log(response);
                if (Object.keys(response).indexOf("actuator1") >= 0){
                    if (response["actuator1"] == 1) {
                        $("#circle0").attr("class", "black");
                    }
                    else {
                        $("#circle0").attr("class", "blue");
                    }
                }
            },
            complete: function(response) {
                setTimeout(get_status, interval);
            }
        });
        }
        setTimeout(get_status, interval);\n""")
    for port in cleaned_port_numbers:
        html.write("""        $('#box""" + port + """').change(function() {
          var status = document.getElementById('toggledbox""" + port + """').innerHTML
          if (status == 'On') {
            $('#toggledbox""" + port + """').html('Off');
          }
          else {
            $('#toggledbox""" + port + """').html('On');
          }
          $.ajax({
                url: "/get_toggled_status",
                type: "GET",
                data: {status: status, port: """ + port + """},
            });
        });\n""")
    html.write("""      });
    </script>
</html>""")
    html.close()

    return render_template('node_1.html')

# proxy
@app.route('/access', methods=['GET'])
def accessor():
    result = requests.get(url='http://128.59.22.210:4000/state')
    return result.text

# check which one sent the toggled status
@app.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')
    port_number = request.args.get('port')

    if current_status == 'On':
        # current testing
        result = requests.post(url="http://128.59.22.210:4000/", data={'actuator1': 1})

        # for the future
        # sending_data = data["open_whisk" + str(port_number)]
        # # container
        # connected = False
        # # need to check which URLs are open
        # while not connected:
        #     result = requests.post(url="http://128.59.22.210:80/", json=sending_data)
        #     sleep(1)
        #     if result.status_code == requests.codes.ok:
        #         connected = True
    else:
        result = requests.post(url="http://128.59.22.210:4000/", data={'actuator1': 0})

    return render_template('node_1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
