

**command to push events**

```sh
./bin/kafka-console-producer.sh --bootstrap-server kafka-headless:9092 --topic dev.system.events < ./output.json
```