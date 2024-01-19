const { faker } = require('@faker-js/faker');

const { IMPRESSION_TYPE, IMPRESSION_SUB_TYPE, MOCK_URI, VISITS_SECTION, ITYPES, PAGE_IDS } = require('../mock');

const config = {
    eid: "impression",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(IMPRESSION_TYPE),
            "subtype": faker.helpers.arrayElement(IMPRESSION_SUB_TYPE),
            "pageid": faker.helpers.arrayElement(PAGE_IDS),
            "uri": faker.helpers.arrayElement(MOCK_URI),
            "duration": faker.datatype.number({ min: 1, max: 60 }),
            "visits": faker.datatype.number({ min: 10, max: 1000 })
        }
    }
}

module.exports = config;
