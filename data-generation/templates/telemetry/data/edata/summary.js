const { faker } = require('@faker-js/faker');

const { SUMMARY_TYPES, SUMMARY_EVENTS_SUMMARY, SUMMARY_ENV_SUMMARY } = require('../mock');

const config = {
    eid: "summary",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(SUMMARY_TYPES), // Required. Type of summary. Free text. "session", "app", "tool" etc
            "mode": faker.helpers.arrayElement(["online", "offline"]), // Optional.
            "starttime": faker.datatype.datetime().getTime(),
            "endtime": faker.datatype.datetime().getTime(),
            "timespent": faker.datatype.number({ min: 10, max: 1000 }),
            "pageviews": faker.datatype.number({ min: 10, max: 1000 }), // Required. Total page views per session(count of CP_IMPRESSION)
            "interactions": faker.datatype.number({ min: 10, max: 1000 }), // Required. Count of interact events
            "envsummary": [
                {
                    "env": faker.helpers.arrayElement(SUMMARY_ENV_SUMMARY), // High level env within the app (content, domain, resources, community)
                    "timespent": faker.datatype.number({ min: 0, max: 100 }), // Time spent per env
                    "visits": faker.datatype.number({ min: 10, max: 1000 }) // count of times the environment has been visited
                }
            ],
            "eventssummary": [
                {
                    "id": faker.helpers.arrayElement(SUMMARY_EVENTS_SUMMARY), // event id such as CE_START, CE_END, CP_INTERACT etc.
                    "count": faker.datatype.number({ min: 10, max: 1000 }) // Count of events.
                }
            ],
            "pagesummary": [
                {
                    "id": faker.datatype.string(),
                    "type": faker.helpers.arrayElement(["view", "edit"]), // type of page - view/edit
                    "env": faker.datatype.string(),
                    "timespent": faker.datatype.number({ min: 10, max: 1000 }), // Time taken per page
                    "visits": faker.datatype.number({ min: 10, max: 1000 }) // Number of times each page was visited
                }]
        }
    }
}

module.exports = config;
