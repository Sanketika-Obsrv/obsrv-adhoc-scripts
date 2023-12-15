const { faker } = require('@faker-js/faker');
const dayjs = require('dayjs');
const _ = require('lodash');
const { getEdata } = require('./data/edata');

const { ACTOR_ID, ACTOR_TYPE, CONTEXT_DID, CONTEXT_ENV, OBJECT_IDENTIFIER, OBJECT_TYPE, PDATA_ID, PDATA_PID, PDATA_PLATFORM, SUMMARY_TYPES, SUMMARY_MODES, DUPLICATE_IDS } = require('./data/mock');
const ETS_GENERATION_DATE_RANGE = { from: "2023-04-01", to: dayjs().format('YYYY-MM-DD') };

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const SummaryService = {
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
        const eventEnvelop = _.cloneDeep(require('./data/summarySpec.js'));
        eventEnvelop.edata = eData;
        eventEnvelop.eid = _.toUpper(eid);
        eventEnvelop.ets = faker.date.between(ETS_GENERATION_DATE_RANGE.from, ETS_GENERATION_DATE_RANGE.to).getTime();
        eventEnvelop.mid = faker.datatype.uuid();

        // update actor object
        eventEnvelop.actor.type = faker.helpers.arrayElement(ACTOR_TYPE);
        // eventEnvelop.actor.id = faker.datatype.uuid();
        eventEnvelop.actor.id = faker.helpers.arrayElement(ACTOR_ID);

        // Update dimension object 
        eventEnvelop.dimension.channel = faker.datatype.uuid();
        // eventEnvelop.dimension.did = faker.datatype.uuid();
        eventEnvelop.dimension.did = faker.helpers.arrayElement(CONTEXT_DID);
        eventEnvelop.dimension.env = faker.helpers.arrayElement(CONTEXT_ENV);
        eventEnvelop.dimension.sid = faker.datatype.uuid();

        eventEnvelop.dimension.type = faker.helpers.arrayElement(SUMMARY_TYPES);
        eventEnvelop.dimension.mode = faker.helpers.arrayElement(SUMMARY_MODES);

        //update dimension pdata object 
        eventEnvelop.dimension.pdata.pid = faker.helpers.arrayElement(PDATA_PID);
        eventEnvelop.dimension.pdata.id = faker.helpers.arrayElement(PDATA_ID);
        eventEnvelop.dimension.pdata.ver = faker.datatype.number({ min: 1, max: 10 }).toString();
        eventEnvelop.dimension.pdata.platform = faker.helpers.arrayElement(PDATA_PLATFORM);
        eventEnvelop.dimension.cdata = [{ type: faker.datatype.uuid(), id: faker.datatype.uuid() }];

        //update context pdata object 
        eventEnvelop.context.pdata.model = "WorkflowSummarizer"
        eventEnvelop.context.pdata.id = "AnalyticsDataPipeline";
        eventEnvelop.context.pdata.ver = "1.0"
        eventEnvelop.context.granularity = "SESSION"
        eventEnvelop.context.date_range.from = faker.date.between(ETS_GENERATION_DATE_RANGE.from, ETS_GENERATION_DATE_RANGE.to).getTime();
        eventEnvelop.context.date_range.to = faker.date.between(ETS_GENERATION_DATE_RANGE.from, ETS_GENERATION_DATE_RANGE.to).getTime();
        eventEnvelop.context.cdata = [{ type: faker.datatype.uuid(), id: faker.datatype.uuid() }];

        eventEnvelop.context.rollup.l1 = faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.context.rollup.l2 = faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.context.rollup.l3 = faker.helpers.arrayElement(OBJECT_IDENTIFIER);
        eventEnvelop.context.rollup.l4 = faker.helpers.arrayElement(OBJECT_IDENTIFIER);

        // update object data
        eventEnvelop.object.id = faker.helpers.arrayElement(OBJECT_IDENTIFIER)
        eventEnvelop.object.ver = faker.datatype.number({ min: 1, max: 4 }).toString()
        eventEnvelop.object.type = faker.helpers.arrayElement(OBJECT_TYPE)
        eventEnvelop.object.rollup.l1 = faker.helpers.arrayElement(OBJECT_IDENTIFIER)
        eventEnvelop.object.rollup.l2 = faker.helpers.arrayElement(OBJECT_IDENTIFIER)
        eventEnvelop.object.rollup.l3 = faker.helpers.arrayElement(OBJECT_IDENTIFIER)
        eventEnvelop.object.rollup.l4 = faker.helpers.arrayElement(OBJECT_IDENTIFIER)
        // update tags
        eventEnvelop.tags = [faker.datatype.uuid()]
        return eventEnvelop
    }
}
module.exports = SummaryService
