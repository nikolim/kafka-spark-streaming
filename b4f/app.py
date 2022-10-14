import os
from threading import Thread
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from kafka import KafkaConsumer

app = Flask(__name__, static_folder='../frontend/build')

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
    consumer = KafkaConsumer('processed', bootstrap_servers='localhost:9092')
    for message in consumer:
        curr_btc_price[0] = message.value.decode('utf-8')
        send_message(btc_price=curr_btc_price[0])

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
