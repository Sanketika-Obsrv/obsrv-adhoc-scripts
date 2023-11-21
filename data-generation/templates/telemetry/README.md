# Sunbird Telemetry Events Generation Utility

This utility allows generation of sample telemetry events based on the Sunbird Telemetry Specification. Useful for generating sample events for writing data products.

### Installation
You will need node/npm installed before installing. 

```shell
cd data-generation/templates/telemetry
npm i
```

### Usage
- Edit config.js for configuring the flow of events and no. of events
```javascript
denormDataSize: 1600,
noOfEventsPerBatch: 100, // How many events to send in 1 batch
totalBatchesToPush: 16, // No. of batches to send. Has to be in multiples of 16
concurrency: 50,
kafkaBrokers: 'kafka-headless:9092', // Comma separated list
kafkaTopic: 'dev.ingest',
apiHost: 'http://localhost:4000/', // Include the / at the end
datasetName: 'telemetry',
pushViaApi: false, // Push the data via API
pushViaKafka: true, // Push the data via Kafka
generateInvalidData: false, // Generate invalid data
```
- Note: totalBatchesToPush=16 and noOfEventsPerBatch=100, it will push 1600 events
- Master data does not use the totalBatches to push. It will push the data as per the denormDataSize mentioned in the config file in batches with 100 events per batch
- Update the kafka brokers/api host accordingly for pushing the data.

- For kafka need to provide the topic as well

### Settings
- By default the script pushes data as batch
- The `extraction_key` property is set to `events`
- The `batch_id` property is set to `id`
- To update the properties based on dataset
    - Line 34 in index.js has to be modified
    - Line 34 in summary.js has to be modified for summary data
    - Line 35 in master.js for masterdata
- Master data please add the respective data variable of which push according to requirement
- To write any data to file, use the script with `ToFile.js` suffix and data would be written into the output folder
