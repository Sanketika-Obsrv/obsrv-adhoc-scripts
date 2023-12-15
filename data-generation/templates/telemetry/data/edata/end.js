const { faker } = require('@faker-js/faker');

const { START_END_TYPE, START_END_MODE, PAGE_IDS, getMockedSummaryObject } = require('../mock');

const config = {
    eid: "end",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(START_END_TYPE),
            "mode": faker.helpers.arrayElement(START_END_MODE),
            "duration": faker.datatype.number({ min: 1, max: 200 }),
            "pageid": faker.helpers.arrayElement(PAGE_IDS),
            "summary": [
                faker.helpers.arrayElement(getMockedSummaryObject())
            ]
        }
    }
}

module.exports = config;