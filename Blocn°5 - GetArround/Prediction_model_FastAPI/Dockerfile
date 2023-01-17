FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update -y 
RUN apt-get install nano unzip
RUN apt-get install -y python3.10
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

COPY . /home/app

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV BACKEND_STORE_URI=$BACKEND_STORE_URI
ENV ARTIFACT_STORE_URI=$ARTIFACT_STORE_URI
ENV MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI

CMD gunicorn app:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker 