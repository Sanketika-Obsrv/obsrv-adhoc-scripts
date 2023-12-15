const uuid = require("uuid");
const fs = require('fs');
const telemetryService = require('./TelemetryService');
const { globalConfig } = require("./config");

let successCounter = 0;
let failedCounter = 0;
let totalBatchesCount = 0;

const saveToFileClosure = (eid, batchSize = globalConfig.noOfEventsPerBatch) => {
    const events = new Array(batchSize).fill(1).map(_ => telemetryService.generateEvents(eid));
    return fs.writeFileSync(`./output/${eid}-${uuid.v4()}.json`, JSON.stringify(events), 'utf-8');
}

(async () => {
    const startTime = Date.now();
    console.log(`Start time - ${startTime}`);
    try {
        const ratio = globalConfig.totalBatchesToPush / 16;
        const eidToBatchMapping = {
            impression: ratio,
            interact: ratio,
            start: ratio,
            end: ratio,
            search: ratio,
            audit: ratio,
            error: ratio,
            assess: ratio,
            exdata: ratio,
            feedback: ratio,
            interrupt: ratio,
            log: ratio,
            metrics: ratio,
            response: ratio,
            share: ratio,
            summary: ratio,
        }

        let tasks = [];

        for (const [eid, batchCount] of Object.entries(eidToBatchMapping)) {
            saveToFileClosure(eid);
        }

        const endTime = Date.now();
        console.log(`End time - ${endTime}`);
        console.log("Time Taken to push batch data", endTime - startTime);
        console.log(`Tasks Count ${totalBatchesCount}`);
        console.log(`Events Count ${totalBatchesCount * globalConfig.noOfEventsPerBatch}`);
        console.log(`Total Successful Batches Count - ${successCounter}`);
        console.log(`Total Failed Batches Count - ${failedCounter}`);
    }
    catch (error) {
        console.log(error);
    }
    finally {
        process.exit()
    }
})()
