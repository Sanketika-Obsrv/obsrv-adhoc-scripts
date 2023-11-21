const { faker } = require('@faker-js/faker');

const { START_END_TYPE, START_END_MODE, PAGE_IDS } = require('../mock');

const config = {
    eid: "start",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(START_END_TYPE),
            "dspec": {
                "id": faker.datatype.uuid()
            },
            "uaspec": {
                "agent": faker.datatype.uuid()
            },
            "loc": faker.datatype.string(),
            "mode": faker.helpers.arrayElement(START_END_MODE),
            "duration": (faker.datatype.number({ min: 1, max: 9 }) * 1000),
            "pageid": faker.helpers.arrayElement(PAGE_IDS)
        }
    }
}

module.exports = config;
