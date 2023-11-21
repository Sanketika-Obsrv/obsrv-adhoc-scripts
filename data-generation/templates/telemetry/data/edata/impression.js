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
            "visits": [{
                "objid": faker.datatype.uuid(),
                "objtype": faker.helpers.arrayElement(["Resource", "Course", "TextBook"]),
                "objver": (faker.datatype.number({ min: 0, max: 1 })).toString(),
                "index": (faker.datatype.number({ min: 1, max: 2 })),
            }]
        }
    }
}

module.exports = config;
