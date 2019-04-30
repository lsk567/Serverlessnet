from flask import Flask
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    # Status check
    return "Hi, this relayer is running.", 200

@app.route('/send', methods=['POST'])
def send():
    # Parse POST data
    # data = requests.form
    # print("Data received: ")
    # print(data)

    # OpenWhisk setup
    # APIHOST = subprocess.check_output("wsk -i property get --apihost", shell=True).split()[3].decode("utf-8") 
    # AUTH_KEY = subprocess.check_output("wsk -i property get --auth", shell=True).split()[2].decode("utf-8")
    APIHOST = "192.168.1.202"
    AUTH_KEY = "23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP" 
    user_pass = AUTH_KEY.split(':')
    
    # In an ideal case, namespace and action should be parsed from requests from switch
    NAMESPACE = 'guest'
    ACTION = 'flip_switch'
    # NAMESPACE = data["namespace"]
    # ACTION = data["action"]

    # Construct trigger url
    url = 'http://' + APIHOST + ':8888' + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION

    # Some params
    PARAMS = {}
    BLOCKING = 'true'
    RESULT = 'true'

    # print(APIHOST)
    # print(AUTH_KEY)
    # Send post request
    response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
    print(response.text)
    
    return response.text

@app.route('/test', methods=['POST'])
def test():
    # APIHOST = subprocess.check_output("wsk -i property get --apihost", shell=True).split()[3].decode("utf-8") 
    # AUTH_KEY = subprocess.check_output("wsk -i property get --auth", shell=True).split()[2].decode("utf-8") 
    APIHOST = "192.168.1.202"
    AUTH_KEY = "23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"
    NAMESPACE = 'guest'
    ACTION = 'hello_world'
    PARAMS = {'name':'Jerry'}
    BLOCKING = 'true'
    RESULT = 'true'

    print(APIHOST)
    print(AUTH_KEY)
    url = 'http://' + APIHOST + ':8888' + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION
    user_pass = AUTH_KEY.split(':')
    response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
    print(response.text)
    
    return response.text

@app.route('/relay', methods=['POST'])
def relay():
    # Receive request from OpenWhisk
    data = requests.form
    actuatorUrl = data["target"]
    # uiApiURL = None

    # Forward action to actuator
    res = requests.post(url=actuatorUrl)
    print(res)

    # Send the update to UI API
    # requests.post(uiApiURL, json=res)
    
    return 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=4997)