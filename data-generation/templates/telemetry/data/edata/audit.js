const { faker } = require('@faker-js/faker');

const { STATES } = require('../mock');

const config = {
    eid: "audit",
    edata: () => {
        return {
            "props": ["status", "updatedOn", "createdOn", "location"],
            "state": faker.helpers.arrayElement(STATES),
            "prevstate": faker.helpers.arrayElement(STATES)
        }
    }
}

module.exports = config;
