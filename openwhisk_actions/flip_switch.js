var rp = require('request-promise');

function main(params) {
    // sends a request back to relayer app
    var options = {
        method: 'POST',
        uri: 'http://172.17.0.1:4997/relay', // Directly trigger actuator to test
        body: {
            target: 'http://172.17.0.1:4998/state' // To generalize this, receive a target thorugh param, hard code for now
        },
        json: true // Automatically stringifies the body to JSON
    };

    return rp(options) // 172.17.0.1 is the docker0 ip, need to automate this later
    .then(function (htmlString) {
        return {msg: htmlString};
    })
    .catch(function (err) {
        throw err;
    });
}
