var axios = require("axios");
const { Kafka } = require("kafkajs");
const uuid = require("uuid");
const _ = require('lodash');
const { globalConfig } = require("../config");

const kafka = new Kafka({
    clientId: "obsrv-telemetry-generator",
    brokers: globalConfig.kafkaBrokers.split(","),
    retry: {
        initialRetryTime: 3000,
        retries: 1,
    },
    connectionTimeout: 5000,
});

const producer = kafka.producer({
    compression: "snappy",
});


const sendEvent = ({ body, headers = {} }, api, kafka, datasetName = globalConfig.datasetName,) => {
    if (api) return apiCall({ body, headers }, datasetName);
    else if (kafka) return kafkaCall(body, datasetName);
};

const apiCall = ({ body, headers = {} }, datasetName = globalConfig.datasetName,) => {
    var data = {
        data: body,
    };
    var config = {
        method: "post",
        url: `${globalConfig.apiHost}obsrv/v1/data/create/${datasetName}`,
        headers: {
            "Content-Type": "application/json",
            ...headers,
        },
        data: data,
    };
    return axios(config);
}

const kafkaCall = async (message = {}, datasetName = globalConfig.datasetName,) => {
    _.set(message, 'dataset', datasetName);
    if (!_.get(message, 'mid')) _.set(message, 'mid', uuid.v1());
    _.set(message, 'syncts', new Date().getTime());

    await producer.connect();
    if(globalConfig.pushIndividualEventsWithMetadata) {
        for (event_data of _.get(message, 'events')) {
            data_id = uuid.v1();
            ts = new Date().getTime();
            let final_event = {
                id: data_id,
                event: event_data,
                syncts: ts,
                dataset: datasetName,
                obsrv_meta: {
                    syncts: ts,
                    processingStartTime: ts,
                    flags: {},
                    timespans: {},
                    error: {},
                    source:{
                        meta:{
                            id: "",
                            connector_type: "api",
                            version: "1.0",
                            entry_source: "api"
                        },
                        trace_id: data_id
                    }
                }
            }
            await producer.send({
                topic: globalConfig.kafkaTopic,
                messages: [{ value: JSON.stringify(final_event) }],
            }).catch(e => console.error(`[kafka-producer error: ] ${e.message}`, e));
        }
    }
    else if(globalConfig.pushIndividualEventsWithoutMetadata) {
        for (event_data of _.get(message, 'events')) {
            await producer.send({
                topic: globalConfig.kafkaTopic,
                messages: [{ value: JSON.stringify(event_data) }],
            }).catch(e => console.error(`[kafka-producer error: ] ${e.message}`, e));
        }
    }
    else {
        await producer.send({
            topic: globalConfig.kafkaTopic,
            messages: [{ value: JSON.stringify(message) }],
        }).catch(e => console.error(`[kafka-producer error: ] ${e.message}`, e));
    }
}

const errorTypes = ['unhandledRejection', 'uncaughtException']
const signalTraps = ['SIGTERM', 'SIGINT', 'SIGUSR2']

errorTypes.map(type => {
    process.on(type, async () => {
        try {
            console.log(`process.on ${type}`)
            await producer.disconnect()
            process.exit(0)
        } catch (err) {
            process.exit(1)
        }
    })
});

signalTraps.map(type => {
    process.once(type, async () => {
        try {
            await producer.disconnect()
        } finally {
            process.kill(process.pid, type)
        }
    })
})

module.exports = { sendEvent }
