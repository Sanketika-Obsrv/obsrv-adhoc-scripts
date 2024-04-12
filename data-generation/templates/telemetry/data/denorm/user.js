const {
    PROPERTY_IDS,
    USER_TYPES,
    CLUSTERS,
    SCHOOL_NAMES,
    SCHOOL_BOARDS,
    USER_SUBTYPES,
    SUBJECTS,
    LANGUAGES,
    GRADES,
    FRAMEWORKS,
    ORG_NAMES,
} = require("../mock");
const { faker } = require("@faker-js/faker");

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

faker.setLocale("en_IND");
const getUserData = (size) => {
    const USER_IDS = PROPERTY_IDS("user", size);
    return USER_IDS.map((user) => {
        const userTypes = [
            USER_TYPES.sample(),
            USER_TYPES.sample(),
            USER_TYPES.sample(),
        ];
        return {
            userid: user,
            firstname: faker.name.firstName(),
            lastname: faker.name.lastName(),
            state: faker.address.state(),
            district: faker.address.county(),
            block: faker.address.streetName(),
            cluster: CLUSTERS.sample(),
            schooludisecode: `${faker.random.numeric(7)}`,
            schoolname: SCHOOL_NAMES.sample(),
            usertype: `${userTypes.join(",")}`,
            usersubtype: `${userTypes
                .map((item) => USER_SUBTYPES[item])
                .join(",")}`,
            board: SCHOOL_BOARDS.sample(),
            rootorgid: `${faker.random.numeric(19)}`,
            orgname: ORG_NAMES.sample(),
            subject: [SUBJECTS.sample()],
            language: [LANGUAGES.sample()],
            grade: [GRADES.sample()],
            framework: FRAMEWORKS.sample(),
            medium: [LANGUAGES.sample()],
            profileusertypes: userTypes.map((item) => ({
                type: item,
                subType: USER_SUBTYPES[item],
            })),
        };
    });
};

module.exports = { getUserData, SUBJECTS };
