ARG FILE_PATH
FROM --platform=linux/x86_64 flink:scala_2.12-java11 as copy-application
USER flink
COPY ./application/ /app/

FROM --platform=linux/x86_64 flink:scala_2.12-java11 as build-connectors-image
USER flink
COPY --from=copy-application /app/*.jar $FLINK_HOME/lib/
COPY --from=copy-application /app/lib/*.jar $FLINK_HOME/lib/



