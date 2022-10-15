FROM openjdk:slim
COPY --from=python:3.9 / /

ENV JAVA_HOME=/usr/local/openjdk-18
ENV KAFKA_BROKER=broker:9092

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . .

CMD [ "python3", "spark.py" ]
