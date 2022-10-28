import os
import requests
from time import sleep

from kafka import KafkaProducer
from concurrent.futures import ThreadPoolExecutor

import logging
logging.basicConfig(level=logging.INFO)

# check if env variables are set (docker) otherwise use localhost
KAFKA_BROKER = os.environ['KAFKA_BROKER']  if "KAFKA_BROKER" in os.environ else "localhost:9092"

# endpoint to get bitcoin price
binanceAPI = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# endpoint to get bitcoin hashrate
blockchainAPI = "https://blockchain.info/q/hashrate"

FREQUNCY = 10

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

# data dict to store the most recent values
data_dict = {"btc_price": 0, "hash_rate": 0}

def send_to_kafka():
	while True:
		future = producer.send('raw', str(data_dict).encode('utf-8'))
		future.get(timeout=60)
		sleep(1/FREQUNCY)

def get_btc_price():
	while True:
		r = requests.get(binanceAPI)
		data_dict['btc_price'] = r.json()['price']
		sleep(1/FREQUNCY)

def get_hash_rate():
	while True:
		r = requests.get(blockchainAPI)
		data_dict['hash_rate'] = r.json()
		sleep(1/FREQUNCY)

if __name__ == "__main__":
	executor = ThreadPoolExecutor(3)
	for func in [get_btc_price, get_hash_rate, send_to_kafka]:
		executor.submit(func)

	executor.shutdown(wait=True)

		


