from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
app = Flask(__name__)

temperature = 0
humidity = 0
waterLevel = 0

app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

@app.route('/')
def index():
    # Subscribe to a topic
    mqtt.subscribe('my/topic')

    # Define a callback function that will be called when a message is received
    def on_message(client, userdata, message):
        print("Received message: " + message.payload.decode("utf-8"))

    # Set the callback function
    mqtt.on_message = on_message

    # Return a response to the user
    return "Subscribed to MQTT broker and listening for messages on 'my/topic'!"

@app.route('/publish')
def publish():
    mqtt.publish('my/topic', 'Hello, World!')
    return  "Sublished hello world"
