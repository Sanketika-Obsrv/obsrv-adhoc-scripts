const globalConfig = {
    denormDataSize: 1600,
    noOfEventsPerBatch: 100,
    totalBatchesToPush: 16, // Has to be in multiples of 16
    concurrency: 25,
    kafkaBrokers: 'localhost:9092',
    kafkaTopic: 'local.input.topic',
    apiHost: 'http://localhost:3000/', // Include the / at the end
    datasetName: 'telemetry',
    pushViaApi: false,
    pushViaKafka: true,
    generateInvalidData: false,
    pushIndividualEventsWithoutMetadata: false, // Only valid with kafka push, doesn't include batch configuration
    pushIndividualEventsWithMetadata: false // Only valid with kafka push, includes obsrv_meta as well
}

module.exports = { globalConfig };
