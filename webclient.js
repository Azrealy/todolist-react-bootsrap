var request = require('request');
var option = {
    url: 'http://localhost:8888',
};

function callback(error, response, body) {
if (!error && response.statusCode === 200) {
    console.log(body);
}
}
request(option, callback);