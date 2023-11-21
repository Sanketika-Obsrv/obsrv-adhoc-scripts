const { faker } = require('@faker-js/faker');
const { PAGE_IDS } = require('../mock');

const config = {
    eid: "interrupt",
    edata: () => {
        return {
            "type": faker.datatype.string(8),
            "pageid": faker.helpers.arrayElement(PAGE_IDS)
        }
    }
}

module.exports = config;
