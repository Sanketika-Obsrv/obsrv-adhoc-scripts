FROM --platform=linux/amd64 flink:scala_2.12-java11

RUN apt-get update \
  && apt-get install -y python3.10 python3-pip \  
  && rm -rf /var/lib/apt/lists/*
# RUN pip install Flask
RUN pip install boto3

ENV AWS_ACCESS_KEY_ID='AWS_ACCESS_KEY_ID'
ENV AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY'

COPY wrapper-api.py /opt/flink/python-files/

# ENTRYPOINT [ "python3.10", "/opt/flink/python-files/wrapper-api.py"]