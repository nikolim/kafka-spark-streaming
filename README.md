### Backend 
```bash 
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt

cd backend
python3 backend
```

### Kafka 
```bash 
cd kafka 
docker-compose up -d
docker-compose down
docker-compose restart
```
### Spark
```bash 
pip3 install -r requirements.txt
```

### Frontend
```bash
cd frontend
flask run
cd react-fronend
yarn install
yarn start
```
