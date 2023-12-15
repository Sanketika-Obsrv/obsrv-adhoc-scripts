const { faker } = require('@faker-js/faker');

const { SUMMARY_EVENTS_SUMMARY, SUMMARY_ENV_SUMMARY } = require('../mock');

const config = {
    eid: "me_workflow_summary",
    edata: () => {
        return {
                "eks": {
                    "interact_events_per_min": faker.datatype.number({ min: 10, max: 1000 }), // Required. Count of interact events
                    "start_time": faker.datatype.datetime().getTime(),
                    "interact_events_count": faker.datatype.number({ min: 10, max: 1000 }), // Required. Count of interact events
                    "item_responses": [],
                    "end_time": faker.datatype.datetime().getTime(),
                    "events_summary": [
                        {
                            "id": faker.helpers.arrayElement(SUMMARY_EVENTS_SUMMARY), // event id such as CE_START, CE_END, CP_INTERACT etc.
                            "count": faker.datatype.number({ min: 10, max: 1000 }) // Count of events.
                        }
                    ],
                    "page_summary": [
                        {
                            "id": faker.datatype.string(),
                            "type": faker.helpers.arrayElement(["view", "edit"]), // type of page - view/edit
                            "env": faker.datatype.string(),
                            "timespent": faker.datatype.number({ min: 10, max: 1000 }), // Time taken per page
                            "visits": faker.datatype.number({ min: 10, max: 1000 }) // Number of times each page was visited
                        }
                    ],
                    "time_diff": faker.datatype.number({ min: 10, max: 1000 }),
                    "env_summary": [
                        {
                            "env": faker.helpers.arrayElement(SUMMARY_ENV_SUMMARY), // High level env within the app (content, domain, resources, community)
                            "timespent": faker.datatype.number({ min: 0, max: 100 }), // Time spent per env
                            "visits": faker.datatype.number({ min: 10, max: 1000 }) // count of times the environment has been visited
                        }
                    ],
                    "time_spent": faker.datatype.number({ min: 10, max: 1000 })
                }
            }
        }
    }

module.exports = config;