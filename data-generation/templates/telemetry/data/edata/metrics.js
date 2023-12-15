const { faker } = require('@faker-js/faker');

const config = {
    eid: "metrics",
    edata: () => {

        const generateMetric = () => ({
            [faker.lorem.word()]: `${faker.datatype.number({ min: 0, max: 100 })}`
        })

        return {
            ...generateMetric(),
            ...generateMetric(),
            ...generateMetric()
        }
    }
}

module.exports = config;
