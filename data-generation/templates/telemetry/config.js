const globalConfig = {
    denormDataSize: 1600,
    noOfEventsPerBatch: 100,
    totalBatchesToPush: 16, // Has to be in multiples of 16
    concurrency: 25,
    kafkaBrokers: 'localhost:9092',
    kafkaTopic: 'local.input.topic',
    apiHost: 'http://localhost:3000/', // Include the / at the end
    datasetName: 'telemetry',
    pushViaApi: true,
    pushViaKafka: false,
    generateInvalidData: false,
}

module.exports = { globalConfig };
