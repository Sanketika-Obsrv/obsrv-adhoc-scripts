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
} = require("./data/mock");
const { getDeviceData } = require("./data/denorm/devices");
const { getUserData } = require("./data/denorm/user");
const { getContentData } = require("./data/denorm/content");
const { getDialCodeData } = require("./data/denorm/dialcode");

const ACTOR_IDS = PROPERTY_IDS("user", globalConfig.denormDataSize);
const CONTENT_IDS = PROPERTY_IDS("content", globalConfig.denormDataSize);
const DEVICE_IDS = PROPERTY_IDS("device", globalConfig.denormDataSize);
const ETS_GENERATION_DATE_RANGE = {
  from: "2023-09-25",
  to: dayjs().format("YYYY-MM-DD"),
};
Array.prototype.sample = function () {
  return this[Math.floor(Math.random() * this.length)];
};

const TelemetryService = {
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
    const eventEnvelop = _.cloneDeep(require("./data/telemetrySpec.js"));
    eventEnvelop.edata = eData;
    eventEnvelop.eid = _.toUpper(eid);
    const ts = faker.date
    .between(ETS_GENERATION_DATE_RANGE.from, ETS_GENERATION_DATE_RANGE.to);
    eventEnvelop.ets = ts.getTime();
    eventEnvelop.mid = faker.datatype.uuid();
    eventEnvelop.syncts = ts.getTime();
    eventEnvelop["@timestamp"] = ts.toISOString();
    // update actor object
    eventEnvelop.actor.type = faker.helpers.arrayElement(ACTOR_TYPE);
    if (eventEnvelop.actor.type === "User")
      eventEnvelop.actor.id = faker.helpers.arrayElement(ACTOR_IDS);
    else eventEnvelop.actor.id = faker.datatype.uuid();

    // Update context object
    eventEnvelop.context.channel = faker.datatype.string(8);
    eventEnvelop.context.did = DEVICE_IDS.sample();
    eventEnvelop.context.env = faker.helpers.arrayElement(CONTEXT_ENV);
    eventEnvelop.context.sid = faker.datatype.uuid();
    if (eventEnvelop.actor.type === "User")
      eventEnvelop.context.uid = faker.helpers.arrayElement(ACTOR_IDS);
    else eventEnvelop.context.uid = faker.datatype.uuid();

    //update context pdata object
    eventEnvelop.context.pdata.pid = faker.helpers.arrayElement(PDATA_PID);
    eventEnvelop.context.pdata.id = faker.helpers.arrayElement(PDATA_ID);
    eventEnvelop.context.pdata.ver = faker.datatype
      .number({ min: 1, max: 10 })
      .toString();
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
      eventEnvelop.object.id = faker.helpers.arrayElement(OBJECT_IDENTIFIER);
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
  }
};
module.exports = TelemetryService;
