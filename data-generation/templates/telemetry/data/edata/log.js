const { faker } = require('@faker-js/faker');

const { LOG_LEVEL, LOG_MESSAGE, LOG_EDATA_TYPES, generateRandomJSON } = require('../mock');

const config = {
    eid: "log",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(LOG_EDATA_TYPES),
            "level": faker.helpers.arrayElement(LOG_LEVEL),
            "message": faker.helpers.arrayElement(LOG_MESSAGE),
            "pageid": faker.datatype.string(8),
            "params": [
                {
                    "foo": faker.datatype.string(7),
                    "bar": faker.datatype.string(7),
                    "bike": faker.datatype.string(7),
                    "a": faker.datatype.string(7),
                    "b": faker.datatype.string(7),
                    "name": faker.datatype.string(7),
                    "prop": faker.datatype.string(7)
                },
                {
                    "foo": faker.datatype.string(7),
                    "bar": faker.datatype.string(7),
                    "bike": faker.datatype.string(7),
                    "a": faker.datatype.string(7),
                    "b": faker.datatype.string(7),
                    "name": faker.datatype.string(7),
                    "prop": faker.datatype.string(7)
                },
            ]
        }
    }
}

module.exports = config;
