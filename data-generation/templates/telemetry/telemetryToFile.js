const uuid = require("uuid");
const fs = require('fs');
const telemetryService = require('./TelemetryService');
const { globalConfig } = require("./config");

let successCounter = 0;
let failedCounter = 0;
let totalBatchesCount = 0;

let globalEvents = [];
const saveToFileClosure = (eid, batchSize = globalConfig.noOfEventsPerBatch, fillCount) => {
    const events = new Array(batchSize).fill(1).map(_ => telemetryService.generateEvents(eid));
    globalEvents = [...globalEvents, ...events];
}

(async () => {
    const startTime = Date.now();
    console.log(`Start time - ${startTime}`);
    try {
        console.log(`Total Batches to push - ${globalConfig.totalBatchesToPush}`)
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
            for (i = 0; i < batchCount; i++) {
                saveToFileClosure(eid);
            }
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
        fs.writeFileSync(`./output/${uuid.v4()}.json`, JSON.stringify(globalEvents), 'utf-8');
        process.exit()
    }
})()
