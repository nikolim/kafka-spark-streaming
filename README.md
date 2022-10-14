## Setup

### Kafka 
```bash 
cd kafka 
docker-compose up -d

# check if everything is running
docker ps

# additional commands
docker-compose down
docker-compose restart
```

### Backend 
```bash 
cd backend
python3 -m venv venv 
source venv/bin/activate

pip3 install -r requirements.txt
python3 backend.py
```

### Spark
Note not working yet
```bash 
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt

python3 spark.py
```

### Backend4Frontend
```bash
cd b4f
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt

python3 app.py
```

### Frontend
```bash
cd fronend
yarn install

# during development
yarn dev

# build to serve via b4f
yarn build
```