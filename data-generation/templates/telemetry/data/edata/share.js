const { faker } = require('@faker-js/faker');
const { PAGE_IDS } = require('../mock');

const config = {
    eid: "share",
    edata: () => {
        return {
            "dir": faker.helpers.arrayElement(["In", "Out"]),
            "type": faker.helpers.arrayElement(["File", "Link", "Message"]),
            "items": [
                {
                    "ver": faker.datatype.number({ min: 1, max: 5, precision: 1 }).toString(),
                    "origin": {
                        "id": faker.datatype.uuid(),
                        "type": faker.helpers.arrayElement(["File", "Link", "Message"])
                    },
                    "id": "content1",
                    "to": {
                        "id": faker.datatype.uuid(),
                        "type": faker.helpers.arrayElement(["File", "Link", "Message"])
                    },
                    "type": "CONTENT",
                    "params": [
                        {
                            "transfers": 0,
                            "count": 0
                        }
                    ]
                }
            ]
        }
    }
}

module.exports = config;
