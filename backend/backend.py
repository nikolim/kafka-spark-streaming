import os
from time import sleep, time
from kafka import KafkaProducer
import requests

KAFKA_BROKER = os.environ['KAFKA_BROKER']  if "KAFKA_BROKER" in os.environ else "localhost:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
binanceAPI = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

while True:
	try:
		data = requests.get(binanceAPI)
		data = data.json()
		bitcoin_price = data["price"]
		future = producer.send('raw', str(bitcoin_price).encode('utf-8'))
		print("Backend sent: " + str(bitcoin_price))
		future.get(timeout=60)
		sleep(0.1)
	except KeyboardInterrupt:
		break