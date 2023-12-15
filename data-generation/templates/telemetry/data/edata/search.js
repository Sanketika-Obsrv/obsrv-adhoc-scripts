const { faker } = require('@faker-js/faker');

const { SEARCH_TYPE, DIAL_CODES, CHANNEL_ID, COURSE_IDS } = require('../mock');

const config = {
    eid: "search",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(SEARCH_TYPE),
            "query": faker.datatype.string(),
            "filters": {
                "dialcodes": faker.helpers.arrayElement(DIAL_CODES),
                "channel": [{
                    "ne": faker.helpers.arrayElement(CHANNEL_ID)
                }]
            },
            "sort": {},
            "correlationid": faker.datatype.string(),
            "size": faker.datatype.number({ min: 10, max: 50 }),
            "topn": [
                {
                    "identifier": faker.helpers.arrayElement(COURSE_IDS)
                }
            ]
        }
    }
}

module.exports = config;
