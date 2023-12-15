const uuid = require("uuid");
const fs = require('fs');
const _ = require('lodash');
const telemetryService = require('./TelemetryService');
const { globalConfig } = require("./config");

let successCounter = 0;
let failedCounter = 0;

const saveToFileClosure = (events, type) => {
    return () => {
        return fs.writeFileSync(`output/${type}-${uuid.v4()}.json`, JSON.stringify(events), 'utf-8')
    }
}

(async () => {
    try {
        const userData = telemetryService.getUserEvents(globalConfig.denormDataSize);
        const dialCodeData = telemetryService.getDialCodeEvents(globalConfig.denormDataSize);
        const deviceData = telemetryService.getDeviceEvents(globalConfig.denormDataSize);
        const contentData = telemetryService.getContentEvents(globalConfig.denormDataSize);
        saveToFileClosure(userData, "users")();
        saveToFileClosure(dialCodeData, "dialCode")();
        saveToFileClosure(deviceData, "device")();
        saveToFileClosure(contentData, "content")();
        console.log("Tasks Count", promises.length);
        console.log("Events Count", promises.length * globalConfig.noOfEventsPerBatch);
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
