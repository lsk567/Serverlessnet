var request = require('request');

var url = 'http://0.0.0.0:4998';

return new Promise(function(resolve, reject) {
    request.get(url, function(error, response, body) {
        if (error) {
            reject(error);
        }
        else {
            var output = body;
            console.log(output);
            resolve({msg: output});
        }
    });
});