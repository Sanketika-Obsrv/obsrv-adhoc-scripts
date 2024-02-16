const { PROPERTY_IDS } = require("../mock");
const { faker } = require("@faker-js/faker");
const { SUBJECTS } = require("./user");
const dayjs = require("dayjs");

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const GRADE_LEVEL = [
    "Class 10",
    "Class 9",
    "Class 11",
    "Class 12",
    "Class 8",
    "Class 7",
    "Class 6",
    "Class 5",
];
const BOOKS = [
    "Mathematics",
    "Science",
    "Physics",
    "Chemistry",
    "Lab",
    "H.C. Verma",
    "Book A",
    "Book B",
];

const ETS_GENERATION_DATE_RANGE = {
    from: "2024-01-17",
    to: dayjs().format("YYYY-MM-DD"),
};
const LANGUAGES = ["Hindi", "English", "Tamil", "Telugu", "Kannada"];
const BOARD = ["CBSE", "ICSE", "State Board"];
const MEDIUM = ["English", "Hindi", "Tamil", "Telugu", "Kannada"];
const STATE = ["Karnataka", "Tamil Nadu", "Andhra Pradesh", "Telangana"];
const DISTRICT = ["Bangalore", "Chennai", "Hyderabad", "Vijayawada"];
const USER_TYPES = ["creator", "anonymous", "authenticated", "teacher", "student", "admin"];


faker.setLocale("en_IND");
const getContentData = (size) => {
    const CONTENT_IDS = PROPERTY_IDS("content", size);
    return CONTENT_IDS.map((content) => {
        return {
            ets: faker.date
                .between(
                    ETS_GENERATION_DATE_RANGE.from,
                    ETS_GENERATION_DATE_RANGE.to
                )
                .getTime(),
            board: BOARD.sample(),
            channel: "012550822176260096119",
            ownershipType: ["createdBy"],
            code: "org.sunbird.kgcdDt",
            description: "Enter description for TextBook",
            organisation: ["diksha_ntptest_org"],
            language: [LANGUAGES.sample()],
            mimeType: "application/vnd.ekstep.content-collection",
            idealScreenSize: "normal",
            createdOn: faker.date
                .between(
                    ETS_GENERATION_DATE_RANGE.from,
                    ETS_GENERATION_DATE_RANGE.to
                )
                .toISOString(),
            appId: "staging.diksha.portal",
            contentDisposition: "inline",
            lastUpdatedOn: faker.date
                .between(
                    ETS_GENERATION_DATE_RANGE.from,
                    ETS_GENERATION_DATE_RANGE.to
                )
                .toISOString(),
            medium: [MEDIUM.sample(), MEDIUM.sample()],
            contentEncoding: "gzip",
            contentType: "TextBook",
            dialcodeRequired: ["Yes", "No"].sample(),
            creator: `suborg_creator_sun ${faker.random.numeric(2)}`,
            createdFor: ["012550822176260096119"],
            lastStatusChangedOn: faker.date
                .between(
                    ETS_GENERATION_DATE_RANGE.from,
                    ETS_GENERATION_DATE_RANGE.to
                )
                .toISOString(),
            audience: [["Learner", "Instructor"].sample()],
            IL_SYS_NODE_TYPE: "DATA_NODE",
            visibility: ["Default", "Parent", "Private"].sample(),
            os: ["All"],
            consumerId: `${faker.datatype.uuid()}`,
            mediaType: "content",
            osId: "org.ekstep.quiz.app",
            version: 2,
            versionKey: "1585729524896",
            idealScreenDensity: "hdpi",
            license: "CC BY 4.0",
            framework: "ekstep_ncert_k-12",
            createdBy: "7a6b150c-08be-4e31-8f69-7fc4b479e61d",
            compatibilityLevel: 1,
            IL_FUNC_OBJECT_TYPE: "Content",
            name: BOOKS.sample(),
            IL_UNIQUE_ID: "do_2129902962679398401472",
            resourceType: "Book",
            status: "Draft",
            mid: `${faker.datatype.uuid()}`,
            label: BOOKS.sample(),
            nodeType: "DATA_NODE",
            userId: "ANONYMOUS",
            objectType: "Content",
            nodeUniqueId: content,
            requestId: faker.random.alphaNumeric(10),
            operationType: ["CREATE", "UPDATE"].sample(),
            nodeGraphId: 215201,
            graphId: "domain"
        };
    });
};

module.exports = { getContentData };
