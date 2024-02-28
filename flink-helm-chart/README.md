**Scala/Java Flink helm chart for connectors**

This helm chart takes the main class name and deploys the connector image on cluster for flink.Additionally it will also take config file specific to the job to run in cluster.

**Command to install helm chart:**
```helm install job-name . -n namespace --set-file job_config=path-to-th-conf-file --set job_classname=main-class-name --set namespace=namespace```

Example:
```helm install kafka-connector . -n flink --set-file job_config=./kafka-connector.conf --set job_classname=org.sunbird.obsrv.kafkaconnector.task.KafkaConnectorStreamTask --set namespace=flink```