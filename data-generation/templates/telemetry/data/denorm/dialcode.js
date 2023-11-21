const { PROPERTY_IDS } = require("../mock");
const { faker } = require('@faker-js/faker');

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const STATUS = ["Draft", "Active", "Inactive", "Invalid", "Retired", "Live"];

faker.setLocale("en_IND");
const getDialCodeData = (size) => {
    const DIAL_CODES = PROPERTY_IDS("dialcode", size);
    return DIAL_CODES.map((content) => ({
        "identifier": content,
        "contextInfo": null,
        "generatedOn": `${faker.date.between('2023-08-24T00:00:00.000Z', '2023-12-01T00:00:00.000Z').toISOString()}`,
        "batchCode": `do_${faker.random.numeric(21)}`,
        "channel": `${faker.random.numeric(20)}`,
        "status": STATUS.sample(),
      }));
};

module.exports = { getDialCodeData }
