## Setup

### Kafka 
```bash 
cd kafka 
docker-compose up -d
docker-compose down
docker-compose restart
docker ps
```

### Backend 
```bash 
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt

cd backend
python3 backend
```

### Spark
```bash 
pip3 install -r requirements.txt
python3 spark.py
```

### Frontend
```bash
cd react-fronend
yarn install
# we are serving the static build
yarn build

pip3 install -r requirements.txt
cd frontend
python3 flask.py
```
