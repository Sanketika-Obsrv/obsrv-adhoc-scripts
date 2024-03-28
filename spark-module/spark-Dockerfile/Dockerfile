FROM --platform=linux/x86_64 sanketikahub/spark:1.0.0-GA as copy-application
ARG FILE_PATH
WORKDIR $SPARK_HOME
USER root
COPY $FILE_PATH /app/

FROM --platform=linux/x86_64 sanketikahub/spark:1.0.0-GA as build-connectors-image
WORKDIR $SPARK_HOME
USER root
COPY --from=copy-application /app/*.jar $SPARK_HOME/jars/
COPY --from=copy-application /app/lib/*.jar $SPARK_HOME/jars/