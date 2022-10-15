FROM node:alpine AS build_stage


COPY /frontend/ /app/frontend

WORKDIR /app/frontend

RUN npm install

RUN npm run build

FROM python:3.9-slim-buster

WORKDIR /app
ENV KAFKA_BROKER=broker:9092

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY --from=build_stage /app/frontend /app/frontend
COPY app.py app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]