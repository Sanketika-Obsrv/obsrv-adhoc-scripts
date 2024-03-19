**Scala/Java Flink helm chart for connectors**

**Build Image**
First, build the image that needs to be deployed in the cluster.

**Command to build the image:**
The command takes as argument the path to the application that contains the jar.

```docker buildx build -f ./flink-Dockerfile/Dockerfile --build-arg FILE_PATH=/path/to/application -t <name>:<tag-name> .```

**Example:**
Consider application is the folder which contains jars needed to run the job, the command to build the image is:

```docker buildx build -f ./flink-Dockerfile/Dockerfile --build-arg FILE_PATH=/path/to/application -t kafka-connector:1.0 .```


**Deploy Image**
This helm chart takes the main class name and deploys the connector image on cluster for flink.Additionally it will also take config file specific to the job to run in cluster.
    
**Command to install helm chart:**

```helm install job-name . -n namespace --set-file job_config=path-to-th-conf-file --set job_classname=main-class-name --set namespace=namespace```

**Example:**

```helm install kafka-connector . -n flink --set-file job_config=./kafka-connector.conf --set job_classname=org.sunbird.obsrv.kafkaconnector.task.KafkaConnectorStreamTask --set namespace=flink```