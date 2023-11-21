const { PROPERTY_IDS } = require("../mock");
const { faker } = require("@faker-js/faker");

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const SUBJECTS = [
    "English",
    "Science",
    "Mathematics",
    "Social",
    "History",
    "Arts",
    "IRCS",
    "Finance",
    "Commerce",
    "Banking",
];
const CLUSTERS = ["CLUSTER1", "CLUSTER2", "CLUSTER3", "CLUSTER4", "CLUSTER5"];
const SCHOOL_NAMES = [
    "DPS, MATHURA",
    "DPS, BANGALORE",
    "DPS, HYDERABAD",
    "DPS, MUMBAI",
    "DPS, DELHI",
];
const ORG_NAMES = [
    "Root Org2",
    "Root Org3",
    "Root Org4",
    "Root Org5",
    "Root Org1",
];
const BOARDS = ["IGOT-Health", "SSC", "CBSE", "ICSE"];
const LANGUAGES = ["Hindi", "English", "Tamil", "Telugu", "Kannada"];
const USER_TYPES = [
    "administrator",
    "administration",
    "teacher",
    "other",
    "parent",
];
const FRAMEWORKS = [
    "igot_health",
    "igot_health_1",
    "igot_health_2",
    "igot_health_3",
    "igot_health_4",
];
const GRADES = [
    "Volunteers",
    "Class 10",
    "Class 9",
    "Class 11",
    "Class 12",
    "Class 8",
    "Class 7",
    "Class 6",
    "Class 5",
];
const USER_SUBTYPES = {
    administration: "hm",
    administrator: "crp",
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
            board: BOARDS.sample(),
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
