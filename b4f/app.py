import os
import json
from threading import Thread
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from kafka import KafkaConsumer

# check if environment variable is set
KAFKA_BROKER = os.environ['KAFKA_BROKER']  if "KAFKA_BROKER" in os.environ else "localhost:9092"

app = Flask(__name__, static_folder='./frontend/build')

# wrap app for socketio
socketio = SocketIO(app, cors_allowed_origins="*")

# get rid of CORS errors
CORS(app)

# use array to pass by reference
curr_btc_price = [0]

@socketio.on("message")
def send_message(btc_price=curr_btc_price[0]):
    socketio.emit("btc", {'price': btc_price})

def consume():
    consumer = KafkaConsumer('processed', bootstrap_servers=KAFKA_BROKER)
    for message in consumer:
        data_obj = json.loads(str(message.value.decode('utf-8')).replace("\'", "\""))
        send_message(btc_price=data_obj['btc_price'])

consume_thread = Thread(target=consume)
consume_thread.start()

# just for testing, not used in production 
@DeprecationWarning
@app.route('/btc')
def get_current_time():
    return {'price': curr_btc_price[0]}

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
