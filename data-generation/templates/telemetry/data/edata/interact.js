const { faker } = require('@faker-js/faker');

const { INTERACT_ID, INTERACT_SUBTYPE, INTERACT_TYPE, PAGE_IDS } = require('../mock');

const config = {
    eid: "interact",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(INTERACT_TYPE),
            "subtype": faker.helpers.arrayElement(INTERACT_SUBTYPE),
            "id": faker.helpers.arrayElement(INTERACT_ID),
            "pageid": faker.helpers.arrayElement(PAGE_IDS),
            "target": {
                id: faker.datatype.string(),
                type: faker.datatype.string(),
                ver: "3.1",
            },
            "plugin": faker.datatype.uuid(),
            "extra": {
                "pos": [
                    {
                        "x": faker.datatype.number({ min: 1, max: 100 }),
                        "y": faker.datatype.number({ min: 1, max: 100 }),
                        "z": faker.datatype.number({ min: 1, max: 100 })
                    }
                ],
                "values": [
                    faker.datatype.datetime().getTime()
                ],
            }
        }
    }
}

module.exports = config;
