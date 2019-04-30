from flask import Flask, render_template, request
import requests, argparse
from time import sleep
import json
import os

app = Flask(__name__)
data = {}

@app.route('/', methods=['GET'])
def node_1_post():
    # gets port numbers and cleans them up
    temp = requests.get(url="http://128.59.21.71:4000/").json()
    port_numbers = temp["port_numbers"]
    cleaned_port_numbers = ['2000']
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

    return render_template('node_1.html')

# check which one sent the toggled status
@app.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')
    port_number = request.args.get('port')

    if current_status == 'On':
        sending_data = data["open_whisk" + str(port_number)]
        print(sending_data)
        # container
        connected = False
        # need to check which URLs are open
        while not connected:
            result = requests.post(url="http://128.59.21.71:4000/", json=sending_data)
            sleep(1)
            if result.status_code == requests.codes.ok:
                connected = True

    return render_template('node_1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')