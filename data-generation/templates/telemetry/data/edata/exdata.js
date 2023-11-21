const { faker } = require('@faker-js/faker');

const config = {
    eid: "exdata",
    edata: () => {
        return {
            "type": faker.helpers.arrayElement(["partnerdata", "xapi"]), // Free flowing text. For ex: partnerdata, xapi etc
            "data": faker.lorem.word()
        }
    }
}

module.exports = config;
