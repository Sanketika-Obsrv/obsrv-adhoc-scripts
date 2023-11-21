const { faker } = require('@faker-js/faker');

const config = {
    eid: "feedback",
    edata: () => {
        return {
            "rating": faker.datatype.number({ min: 1, max: 5 }),
            "comments": faker.lorem.words()
        }
    }
}

module.exports = config;
