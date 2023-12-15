const { faker } = require('@faker-js/faker');

const { ERROR_CODES, ERROR_TYPES, ERROR_STACKTRACE, PAGE_IDS } = require('../mock');

const config = {
    eid: "error",
    edata: () => {
        return {
            "err": faker.helpers.arrayElement(ERROR_CODES),
            "errtype": faker.helpers.arrayElement(ERROR_TYPES),
            "stacktrace": faker.helpers.arrayElement(ERROR_STACKTRACE),
            "pageid": faker.helpers.arrayElement(PAGE_IDS),
            "plugin": faker.datatype.uuid()
        }
    }
}

module.exports = config;