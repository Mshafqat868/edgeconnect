#!flask/bin/python
from flask import Flask, jsonify, request, render_template
import os
import flask_pymongo
from flask_pymongo import MongoClient
import datetime
import paho.mqtt.client as mqtt
from bson.json_util import loads, dumps


cluster = MongoClient(
    'mongodb+srv://shafqat:shafqat@cluster0.rtgng.azure.mongodb.net/edgeconnect?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE', 27017)
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
app = Flask(__name__)
print(cluster)
db = cluster['edgeconnect']
collection = db['devices']
# Hello world endpoint


@app.route('/')
def hello():
    return render_template("index.html")
# Verify the status of the microservice


@app.route('/deviceList')
def deviceList():
    cursor = list(collection.find({}))
    cursor = dumps(cursor)
    return cursor


@app.route('/<id>')
def devicetelemetery(id):
    cursor = list(db[str(id)].find({}))
    cursor = dumps(cursor)
    return cursor
# Get environment details


@app.route('/telemeteryData')
def telemetery_data():
    cursor = list(db['telemetery'].find({}))
    cursor = dumps(cursor)
    return cursor


@app.route('/telemetery', methods=['POST'])
def telemetery():
    print(request.json['imei'])
    db['telemetery'].update_one(
        {"imei": request.json['imei']}, {"$set": request.json}, upsert=True)
    insert_u = db[str(request.json['imei'])].insert_one(
        request.json).inserted_id
    print("here")
    print(insert_u)
    return str(insert_u) + " has been added"


@ app.route('/registration', methods=['POST'])
def environment():
    print(request.json['imei'])
    insert_id = collection.update_one(
        {"imei": request.json['imei']}, {"$set": request.json}, upsert=True).raw_result
    print("here")
    print(insert_id)
    return str(insert_id)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("shafqat")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.payload.decode('utf-8'))
    if msg.payload.decode('utf-8') == "shafqat":
        print("compared successful")

    cluster.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()
if __name__ == '__main__':
    app.run()
