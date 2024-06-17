FROM --platform=linux/amd64 surabhi1510/spark-base-image:1.1
WORKDIR $SPARK_HOME
USER root
ENV RUNTIME="spark"
RUN apt-get update \
&& apt-get install -y python3 python3-pip git vim wget\ 
&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY ./object_store_connector/requirements.txt requirements.txt
RUN pip install git+https://github.com/Sanketika-Obsrv/obsrv-python-sdk.git
RUN pip install boto3 requests
COPY ./wrapper.py /opt/bitnami/spark/python-files/
COPY ./jdbc_connector.conf /opt/bitnami/spark/conf/
COPY ./dependencies/* /opt/bitnami/spark/jars/
COPY ./object_store_connector/* /opt/bitnami/spark/python-files/object_store_connector/

