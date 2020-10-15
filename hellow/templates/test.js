var mqtt = require('mqtt')
var client = mqtt.connect('mqtt://broker.hivemq.com')

client.on('connect', function () {
    client.subscribe('shafqat', function (err) {
        if (!err) {
            client.publish('shafqat', 'Hello mqtt')
        }
    })
})

client.on('message', function (topic, message) {
    // message is Buffer
    console.log(message.toString())
    client.end()
})