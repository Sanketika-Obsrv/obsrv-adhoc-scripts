const { faker } = require('@faker-js/faker');

const { STATES, generateRandomJSON } = require('../mock');

const config = {
    eid: "assess",
    edata: () => {
        return {
            "duration": faker.datatype.number({ min: 0, max: 100 }),
            "item": {
                "desc": faker.lorem.words(),
                "exlength": faker.datatype.number({ min: 0, max: 100 }),
                "id": faker.datatype.uuid(),
                "maxscore": faker.datatype.number({ min: 0, max: 100 }),
                "params": [
                    generateRandomJSON()
                ],
                "uri": faker.lorem.word()
            },
            "pass": faker.helpers.arrayElement(["Yes", "No"]),
            "resvalues": [
                {
                    [`ans${faker.datatype.number({ min: 1, max: 100 })}`]: faker.datatype.number({ min: 0, max: 100 })
                }
            ],
            "score": faker.datatype.number({ min: 0, max: 100 })
        }
    }
}

module.exports = config;
