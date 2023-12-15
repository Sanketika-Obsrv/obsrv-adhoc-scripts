const { faker } = require('@faker-js/faker');

const { STATES, RESPONSE_EDATA_TYPES } = require('../mock');

const config = {
    eid: "response",
    edata: () => {
        return {
            "target": {
                id: faker.datatype.string(),
                type: faker.datatype.string(),
                ver: "3.1",
            },
            "type": faker.helpers.arrayElement(RESPONSE_EDATA_TYPES),
            "values":
                [
                    { "lhs": faker.datatype.string() },
                    { "rhs": faker.datatype.string() }
                ]
        }
    }
}

module.exports = config;
