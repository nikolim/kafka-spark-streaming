from concurrent.futures import thread
import time
from flask import Flask
from kafka import KafkaConsumer
from threading import Thread

app = Flask(__name__)

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
