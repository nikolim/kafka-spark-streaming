# Spark-Kafka-Streaming

## Architecture 

![architecture](architecture.png)

## Deployment Setup 

### Start 
```bash 
docker-compose up 

# if bitcoin price is 0, try restarting b4f
docker-compose restart -t 10 b4f

# or use detached mode
docker-compose up -d 
```
Open frontend on http://localhost:5000

### Stop
```bash 
docker-compose down # run the command inside this repository
```

## Local Development Setup

### 0.Virtual environment
For development we can use a single virtual environment.
```bash 
python3 -m venv venv 
# repeat this step when you open a new terminal or configure the virtual environment in your IDE.
source venv/bin/activate

# to make sure the virtual environment is activated, check path of the python interpreter
which python
```
### 1.Kafka 
First start the kafka broker. Topics will be created automatically by the library.
```bash 
cd kafka 
docker-compose up -d

# check if everything is running
# it might take a couple of seconds
docker ps

# stop the broker once you are done
docker-compose down

# restart if a container crashes
docker-compose restart
```

### 2.Backend 
First start the backend to fetch data from an API.
```bash 
cd backend
pip3 install -r requirements.txt
python3 backend.py
```

### 3.Spark
Consumes the "raw" topic from the backend, and publishes to the "processed" topic.
```bash 
# might slighty differ on your machine (run "which java" to see the path)
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk

pip3 install -r requirements.txt
python3 spark.py
```

### 4.Backend4Frontend
Create flask server to consume the "processed" data and host the react frontend on http://localhost:5000.
```bash
cd b4f
pip3 install -r requirements.txt

python3 app.py
```

### 5.Frontend
For development you can use "yarn start" to get auto-reloading. If you want to hosted version via b4f, you have to build the project.
```bash
cd b4f/fronend
yarn install

# during development
yarn start

# build to serve static files via b4f
yarn build
```