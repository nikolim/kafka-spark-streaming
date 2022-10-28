import os
from time import sleep, time
from kafka import KafkaProducer
import requests

KAFKA_BROKER = os.environ['KAFKA_BROKER']  if "KAFKA_BROKER" in os.environ else "localhost:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
binanceAPI_BTC = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" #can probably have an list of symbols
binanceAPI_ETH = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

## some other apis
# price and hash rate: https://api.minerstat.com/v2/coins?list=BTC

while True:
	try:
		data_BTC = requests.get(binanceAPI_BTC)
		data_ETH = requests.get(binanceAPI_ETH)

		data1 = data_BTC.json()
		data2 = data_ETH.json()

		price = {"BTC": data1["price"], "ETH": data2["price"]}
		# future = producer.send('raw', str(price).encode('utf-8'))
		print("Backend sent: " + str(price))
		# future.get(timeout=60)
		sleep(1)
	except KeyboardInterrupt:
		break