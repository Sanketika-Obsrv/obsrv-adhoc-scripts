const { faker } = require("@faker-js/faker");
const dayjs = require("dayjs");
const _ = require("lodash");
const { getEdata } = require("./data/edata");
const { globalConfig } = require("./config");
const {
    ACTOR_TYPE,
    CONTEXT_ENV,
    OBJECT_IDENTIFIER,
    OBJECT_TYPE,
    PDATA_ID,
    PDATA_PID,
    PDATA_PLATFORM,
    PROPERTY_IDS,
    // ACTOR_IDS,
    DUPLICATE_IDS,
    CHANNEL_ID,
    MEDIUM,
    DISTRICT,
    STATE,
    USER_TYPES,
    SUBJECTS,
    GRADE_LEVEL,
    BOARD,
} = require("./data/mock");
const { getDeviceData } = require("./data/denorm/devices");
const { getUserData } = require("./data/denorm/user");
const { getContentData } = require("./data/denorm/content");
const { getRollupContentData } = require("./data/denorm/rollup-content");
const { getDialCodeData } = require("./data/denorm/dialcode");

const ACTOR_IDS = PROPERTY_IDS("user", globalConfig.denormDataSize);
const CONTENT_IDS = PROPERTY_IDS("content", globalConfig.denormDataSize);
const DEVICE_IDS = PROPERTY_IDS("device", globalConfig.denormDataSize);
const ITEM_IDS = PROPERTY_IDS("item", globalConfig.denormDataSize);
const ETS_GENERATION_DATE_RANGE = {
    from: "2024-02-01T00:00:00.000Z",
    to: `${dayjs().format("YYYY-MM-DD")}T23:59:59.000Z`,
};
Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const MEDIUMS_ARR = [MEDIUM.sample(), MEDIUM.sample()];
const SUBJECTS_ARR = [SUBJECTS.sample(), SUBJECTS.sample()];
const GRADES_ARR = [GRADE_LEVEL.sample(), GRADE_LEVEL.sample()];

const TelemetryRollupService = {
    generateInvalidEvents(eid) {
        var eData = this.getEventData(eid);
        if (!eData) return null;
        const event = this.updateEventEnvelop(_.cloneDeep(eData), eid);
        event.mid = `invalid-mid-${faker.datatype.uuid()}`;
        event.eid = 123;
        event.actor.type = 123;
        return event;
    },
    generateDuplicateEvents(eid) {
        var eData = this.getEventData(eid);
        if (!eData) return null;
        const event = this.updateEventEnvelop(_.cloneDeep(eData), eid);
        event.mid = DUPLICATE_IDS.sample();
        return event;
    },
    generateEvents(eid) {
        var eData = this.getEventData(eid);
        if (!eData) return null;
        return this.updateEventEnvelop(_.cloneDeep(eData), eid);
    },
    getEventData(eid) {
        return getEdata(eid.toLowerCase());
    },
    updateEventEnvelop(eData, eid) {
        let eventEnvelop = _.cloneDeep(require("./data/telemetrySpec.js"));
        eventEnvelop.edata = eData;
        eventEnvelop.edata = {
            ...eData,
            item: {
                id: ITEM_IDS.slice(0, 2).sample(),
                title: [
                    "Sample Title",
                    "Sample Title 1"
                ].sample(),
                maxscore: [40, 50].sample(),
            },
            state: ["Draft", "Live", "Unlisted"].sample(),
            type: [
                "Resource",
                "Collection",
                "TextBook",
                "LessonPlan",
                "Course",
                "CourseUnit",
                "CourseSection",
                "CourseResource",
                "CourseUnitResource",
                "CourseSectionResource",
                "CourseUnitSectionResource",
                "CourseUnitSection",
                "CourseUnitSection",
            ].slice(0, 2).sample(),
            // modes: "preview", "create", "import", "export", "review", "copy", "upload", "update", "delete", "publish", "unpublish", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review", "update", "create", "delete", "upload", "copy", "import", "export", "flag", "unflag", "rate", "review",
            mode: ["edit", "play", "update", "create"].sample(),
            size: [40, 50].sample(),
            duration: [40, 50].sample(),
            score: [40, 50].sample(),
            rating: [1, 2, 3, 4, 5].sample(),
            timespent: [40, 50].sample(),
            pageviews: [40, 50].sample(),
            interactions: [40, 50].sample(),
        };
        eventEnvelop.eid = _.toUpper(eid);
        const contentData = getRollupContentData(MEDIUMS_ARR, GRADES_ARR, SUBJECTS_ARR);
        const ts = faker.date.between(
            ETS_GENERATION_DATE_RANGE.from,
            ETS_GENERATION_DATE_RANGE.to
        );
        eventEnvelop.ets = ts.getTime();
        eventEnvelop.mid = faker.datatype.uuid();
        eventEnvelop.syncts = ts.getTime();
        eventEnvelop["@timestamp"] = ts.toISOString();
        // update actor object
        eventEnvelop.actor.type = faker.helpers.arrayElement(ACTOR_TYPE);
        const actor_id = faker.helpers.arrayElement(ACTOR_IDS);
        if (eventEnvelop.actor.type === "User")
            eventEnvelop.actor.id = actor_id;
        eventEnvelop.actor.id = faker.datatype.uuid();

        // Update context object
        eventEnvelop.context.channel = CHANNEL_ID.slice(0, 2).sample();
        eventEnvelop.context.did = DEVICE_IDS.sample();
        eventEnvelop.context.env = faker.helpers.arrayElement(CONTEXT_ENV);
        eventEnvelop.context.sid = faker.datatype.uuid();
        if (eventEnvelop.actor.type === "User")
            eventEnvelop.context.uid = actor_id;
        eventEnvelop.context.uid = faker.datatype.uuid();

        //update context pdata object
        eventEnvelop.context.pdata.pid = faker.helpers.arrayElement(PDATA_PID.slice(0, 2));
        eventEnvelop.context.pdata.id = faker.helpers.arrayElement(PDATA_ID.slice(0, 2));
        eventEnvelop.context.pdata.ver = [1, 2, 3, 4].sample().toString();
        eventEnvelop.context.pdata.platform =
            faker.helpers.arrayElement(PDATA_PLATFORM);
        eventEnvelop.context.cdata = [
            { type: faker.datatype.uuid(), id: faker.datatype.uuid() },
        ];

        eventEnvelop.context.rollup.l1 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.context.rollup.l2 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.context.rollup.l3 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.context.rollup.l4 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);

        // update object data
        eventEnvelop.object.ver = faker.datatype
            .number({ min: 1, max: 4 })
            .toString();
        eventEnvelop.object.type = faker.helpers.arrayElement(OBJECT_TYPE);
        if (eventEnvelop.object.type === "Content")
            eventEnvelop.object.id = faker.helpers.arrayElement(CONTENT_IDS);
        else
            eventEnvelop.object.id =
                faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.object.rollup.l1 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.object.rollup.l2 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.object.rollup.l3 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.object.rollup.l4 =
            faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        // update tags
        eventEnvelop.tags = [faker.datatype.uuid(), faker.datatype.uuid()];
        const contactType = ["phone", "email"].sample();
        eventEnvelop = {
            ...eventEnvelop,
            contentdata: {
                ...contentData,
            },
            derivedlocationdata: {
                state: STATE.slice(0, 2).sample(),
                district: DISTRICT.slice(0, 2).sample(),
                from: "012550822176260096119",
            },
            collectiondata: {
                name: "TextBook",
                contenttype: "TextBook",
                board: BOARD.slice(0, 2).sample(),
                medium: MEDIUMS_ARR,
                subject: SUBJECTS_ARR,
                gradelevel: GRADES_ARR,
            },
            dialcodedata: {
                channel: CHANNEL_ID.slice(0, 2).sample(),
            },
            userdata: {
                usertype: USER_TYPES.slice(0, 2).sample(),
                usersignintype: contactType,
                userlogintype: contactType,
            },
        };

        return eventEnvelop;
    },
    getDeviceEvents(size) {
        return getDeviceData(size);
    },
    getUserEvents(size) {
        return getUserData(size);
    },
    getContentEvents(size) {
        return getContentData(size);
    },
    getDialCodeEvents(size) {
        return getDialCodeData(size);
    },
};
module.exports = TelemetryRollupService;
