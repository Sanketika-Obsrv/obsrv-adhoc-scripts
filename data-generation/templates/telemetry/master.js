const uuid = require("uuid");
const async = require('async');
const { sendEvent } = require("./utils/api");
const _ = require('lodash');
const telemetryService = require('./TelemetryService');
const { globalConfig } = require("./config");

let successCounter = 0;
let failedCounter = 0;

const makeAsyncBatchCalls = (tasks) => {
    return async.eachLimit(tasks, globalConfig.concurrency, async (batch) => {
        try {
            await batch();
            successCounter += 1;
            console.log(`Success ${successCounter}`);
        } catch (error) {
            console.log(error);
            failedCounter += 1;
            console.log(`Failed ${failedCounter}`);
        }
    });
};

const httpRequestClosure = (events, batchSize = globalConfig.noOfEventsPerBatch,) => {
    const eventsData = _.chunk(events, batchSize);
    const data = eventsData.map((batch) => {
        const body = { id: uuid.v4(), events: batch }
        return () => sendEvent({ body }, globalConfig.pushViaApi, globalConfig.pushViaKafka);
    })
    return data;
}

(async () => {
    try {
        const userData = telemetryService.getUserEvents(globalConfig.denormDataSize);
        const dialCodeData = telemetryService.getDialCodeEvents(globalConfig.denormDataSize);
        const deviceData = telemetryService.getDeviceEvents(globalConfig.denormDataSize);
        const contentData = telemetryService.getContentEvents(globalConfig.denormDataSize);
        const promises = httpRequestClosure(contentData,);
        console.log("Tasks Count", promises.length);
        console.log("Events Count", promises.length * globalConfig.noOfEventsPerBatch);
        await makeAsyncBatchCalls(promises);
        console.log(`Successful Batches Count - ${successCounter}`);
        console.log(`Failed Batches Count - ${failedCounter}`);
    }
    catch (error) {
        console.log(error);
    }
    finally {
        process.exit()
    }
})()
