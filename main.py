import collections.abc
collections.MutableMapping = collections.abc.MutableMapping
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
app = Flask(__name__)

temperature = 0
humidity = 0
waterLevel = 0



eventlet.monkey_patch()

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = "api.allthingstalk.io"
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = "maker:48TaR7AUfdP03vSNudzYqLrQpFgRT0KNVFmi4M7b"
app.config['MQTT_PASSWOfRD'] = 'xxxxxx'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['ATT_DEVICE_ID'] = "JWk8gr0kfTyh6XMnxIfLBENp"


cors = CORS(app, resources={r"*": {"origins": "*"}})
mqtt = Mqtt(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app,cors_allowed_origins='*', async_mode="eventlet")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('device/JWk8gr0kfTyh6XMnxIfLBENp/asset/Temp_ofzo/feed')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)
    print(data)

@app.route('/')
def index():
    return render_template('index.html')

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, use_reloader=False, debug=True)
