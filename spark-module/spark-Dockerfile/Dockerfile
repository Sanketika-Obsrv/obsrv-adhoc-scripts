FROM --platform=linux/x86_64 sanketikahub/spark:1.0.0-GA
WORKDIR $SPARK_HOME
USER root

RUN apt-get update \
  && apt-get install -y python3.10 python3-pip \  
  && rm -rf /var/lib/apt/lists/*
RUN pip install boto3
RUN pip install requests

COPY wrapper-api.py /opt/bitnami/spark/python-files/