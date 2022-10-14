from time import sleep, time
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers='localhost:9092')
binanceAPI = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

while True:
	try:
		data = requests.get(binanceAPI)
		data = data.json()
		bitcoin_price = data["price"]
		future = producer.send('raw', str(bitcoin_price).encode('utf-8'))
		print("Sent: " + str(bitcoin_price))
		future.get(timeout=60)
		sleep(0.1)
	except KeyboardInterrupt:
		break