const uuid = require("uuid");
const fs = require('fs');
const async = require('async');
const { sendEvent } = require("./utils/api");
const summaryService = require('./SummaryService');
const { globalConfig } = require("./config");

let successCounter = 0;
let failedCounter = 0;
let totalBatchesCount = 0;
let batchesCount = {
    'valid': 0,
    'invalid': 0,
    'duplicate': 0,
};

const makeAsyncBatchCalls = (tasks) => {
    return async.eachLimit(tasks, globalConfig.concurrency, async (batch) => {
        try {
            await batch().sendEvent;
            successCounter += 1;
            console.log(`Success ${successCounter}`);
        } catch (error) {
            console.log(error.response);
            failedCounter += 1;
            batchesCount[batch().type] -= 1;
            console.log(`Failed to push batch of type - ${batch().type}`);
        }
    });
};

const httpRequestClosureInvalid = (eid, batchSize = globalConfig.noOfEventsPerBatch) => {
    const events = new Array(batchSize).fill(1).map(_ => summaryService.generateInvalidEvents(eid))
    const body = { id: uuid.v4(), events: events };
    // return events;
    // sendEvent - {body, headers}, //via api - boolean, via kafka - boolean
    return () => ({
        sendEvent: sendEvent({ body }, globalConfig.pushViaApi, globalConfig.pushViaKafka),
        type: 'invalid'
    })
}

const httpRequestClosureDuplicate = (eid, batchSize = globalConfig.noOfEventsPerBatch) => {
    const events = new Array(batchSize).fill(1).map(_ => summaryService.generateDuplicateEvents(eid))
    const body = { id: uuid.v4(), events: events };
    // return events;
    // sendEvent - {body, headers}, //via api - boolean, via kafka - boolean
    return () => ({
        sendEvent: sendEvent({ body }, globalConfig.pushViaApi, globalConfig.pushViaKafka),
        type: 'duplicate'
    })
}

const httpRequestClosure = (eid, batchSize = globalConfig.noOfEventsPerBatch) => {
    const events = new Array(batchSize).fill(1).map(_ => summaryService.generateEvents(eid))
    const body = { id: uuid.v4(), events: events };
    // return events;
    // sendEvent - {body, headers}, //via api - boolean, via kafka - boolean
    return () => ({
        sendEvent: sendEvent({ body }, globalConfig.pushViaApi, globalConfig.pushViaKafka),
        type: 'valid'
    })
}

(async () => {
    const startTime = Date.now();
    console.log(`Start time - ${startTime}`);
    try {
        // const ratio = globalConfig.totalBatchesToPush / 16;
        const eidToBatchMapping = {
            ME_WORKFLOW_SUMMARY: globalConfig.totalBatchesToPush
        }

        let tasks = [];

        for (const [eid, batchCount] of Object.entries(eidToBatchMapping)) {
            for (i = 0; i < batchCount; i++) {
                if(globalConfig.generateInvalidData) {
                    if(i % 8 === 3) {
                        tasks.push(httpRequestClosureInvalid(eid, globalConfig.noOfEventsPerBatch));
                        batchesCount['invalid'] += 1;
                    } else if (i % 8 === 2) {
                        tasks.push(httpRequestClosureDuplicate(eid, globalConfig.noOfEventsPerBatch));
                        batchesCount['duplicate'] += 1;
                    } else {
                        tasks.push(httpRequestClosure(eid, globalConfig.noOfEventsPerBatch));
                        batchesCount['valid'] += 1;
                    }
                } else {
                    tasks.push(httpRequestClosure(eid, globalConfig.noOfEventsPerBatch));
                    batchesCount['valid'] += 1;
                }
                totalBatchesCount += 1;
                if (tasks.length % 1000 === 0) {
                    await makeAsyncBatchCalls(tasks);
                    console.log("Pushed Batch of 1000 batches");
                    console.log(`Successful Batches Count - ${successCounter}`);
                    console.log(`Failed Batches Count - ${failedCounter}`);
                    tasks = [];
                }
            };
        }
        await makeAsyncBatchCalls(tasks);

        const endTime = Date.now();
        console.log(`End time - ${endTime}`);
        console.log("Time Taken to push batch data", endTime - startTime);
        console.log(`Tasks Count ${totalBatchesCount}`);
        console.log(`Total Invalid Batches Count - ${batchesCount['invalid']}`);
        console.log(`Total Duplicate Batches Count - ${batchesCount['duplicate']}`);
        console.log(`Total Valid Batches Count - ${batchesCount['valid']}`);
        console.log(`Valid Events Count ${batchesCount['valid'] * globalConfig.noOfEventsPerBatch}`);
        console.log(`Invalid Events Count ${batchesCount['invalid'] * globalConfig.noOfEventsPerBatch}`);
        console.log(`Duplicate Events Count ${batchesCount['duplicate'] * globalConfig.noOfEventsPerBatch}`);
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
 