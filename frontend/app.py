import os
from threading import Thread

from flask import Flask, send_from_directory
from kafka import KafkaConsumer

app = Flask(__name__, static_folder='react-frontend/build')

curr_btc_price = [0]

def consume():
    consumer = KafkaConsumer('raw', bootstrap_servers='localhost:9092')
    for message in consumer:
        curr_btc_price[0] = message.value.decode('utf-8')

consume_thread = Thread(target=consume)
consume_thread.start()

@app.route('/btc')
def get_current_time():
    return {'price': curr_btc_price[0]}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)
