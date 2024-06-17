import boto3
import zipfile
import os
import shutil
from io import BytesIO
from urllib.parse import urlparse
import logging
import psycopg2
import psycopg2.extras
import subprocess
import tarfile

class ConnectorRuntime():
    def __init__(self):
        self.runtime = os.getenv("RUNTIME")
        self.instances = dict()

    def get_instances(self):
        # get all Live instances based on the runtime
        instances = []
        connection = psycopg2.connect(database="obsrv", user="postgres", password="postgres", host="postgresql.postgresql.svc.cluster.local", port=5432)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
            SELECT ci.*, cr.source_url, cr.technology
            FROM connector_instances as ci
            JOIN connector_registry cr on ci.connector_id = cr.id
            WHERE ci.status = 'Live';
        """
        cursor.execute(query)
        instances = cursor.fetchall()
        for row in instances:
            self.instances[row['connector_id']] = row

    def download_package(self, instance_id):
        # download the package from the source_url using wget and subprocess
        source_url = self.instances[instance_id]['source_url']
        tmp = '/tmp'
        if source_url != None:
            subprocess.run(["wget", source_url, "-O", "{}.tar.gz".format(instance_id)])
            self.extract_file("{}.tar.gz".format(instance_id), tmp)
        for root, dirs, files in os.walk(tmp):
            for file in files:
                source_path = os.path.join(root, file)
                if os.path.basename(root) == 'dependencies':
                    if self.runtime == 'spark':
                        destination_dir = '/opt/bitnami/spark/jars/'
                    elif self.runtime == 'flink':
                        destination_dir = '/opt/flink/lib'
                    else:
                        continue
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir, exist_ok=True)
                    shutil.copy(source_path, destination_dir)
                elif os.path.basename(root) == 'application':
                    destination_dir = f'/data/connectors/'
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir, exist_ok=True)
                    shutil.copy(source_path, destination_dir)
                else:
                    continue
            
    def extract_file(self, tar_path, extract_path):
        print(f"Extracting {tar_path} to {extract_path}")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=extract_path)
        print(f"Extraction complete for {tar_path}")

    def download_packages(self):
        for instance_id, instance in self.instances.items():
            print("Downloading package for id - ", instance_id)
            self.download_package(instance_id)

if __name__ == "__main__":  
    runtime = ConnectorRuntime()
    runtime.get_instances()
    runtime.download_packages()

    