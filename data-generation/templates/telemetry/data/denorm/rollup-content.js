const {
    PROPERTY_IDS,
    BOOKS,
    GRADE_LEVEL,
    SUBJECTS,
    BOARD,
    MEDIUM,
    LANGUAGES,
} = require("../mock");
const { faker } = require("@faker-js/faker");
const dayjs = require("dayjs");
const { globalConfig } = require("../../config");

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const ETS_GENERATION_DATE_RANGE = {
    from: "2024-01-17",
    to: dayjs().format("YYYY-MM-DD"),
};

content_ids = PROPERTY_IDS("content", globalConfig.denormDataSize);

faker.setLocale("en_IND");
const getRollupContentData = (MEDIUMS, GRADES_ARR, SUBJECTS_ARR) => {
    return {
        ets: faker.date
            .between(
                ETS_GENERATION_DATE_RANGE.from,
                ETS_GENERATION_DATE_RANGE.to
            )
            .getTime(),
        board: BOARD.slice(0, 2).sample(),
        channel: "012550822176260096119",
        ownershipType: ["createdBy"],
        code: "org.sunbird.kgcdDt",
        description: "Enter description for TextBook",
        organisation: ["diksha_ntptest_org"],
        language: [LANGUAGES.slice(0, 2).sample()],
        mimeType: "application/vnd.ekstep.content-collection",
        mimetype: "application/vnd.ekstep.content-collection",
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
        medium: MEDIUMS,
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
        nodeUniqueId: content_ids.sample(),
        requestId: faker.random.alphaNumeric(10),
        operationType: ["CREATE", "UPDATE"].sample(),
        nodeGraphId: 215201,
        graphId: "domain",
        gradelevel: GRADES_ARR,
        subject: SUBJECTS_ARR,
    };
};

module.exports = { getRollupContentData };
