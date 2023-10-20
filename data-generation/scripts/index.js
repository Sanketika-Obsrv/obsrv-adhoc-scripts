
const fs = require('fs-extra');
const jsf = require('json-schema-faker');
const _ = require('lodash');
const { faker } = require('@faker-js/faker');

const generate = (schema) => {
    return jsf.generate(schema);
}

const applyNumberConditions = (conditions, event) => {
    let data;
    for (const condition in conditions) {

        if (condition === 'faker') {
            return _.toNumber(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 
        if (condition === '<=') {
            const fields =  _.isArray(conditions["<="]) ? conditions["<="] : Array.from(conditions["<="])
            const fieldsData = _.map(fields, (field) => event[field])
            const minValue = _.min(fieldsData)
            data = faker.number.int({min: 0, max: minValue+1})
        } else if (condition === '>=') {
            const fields =  _.isArray(conditions[">="]) ? conditions[">="] : Array.from(conditions[">="])
            const fieldsData = _.map(fields, (field) => event[field])
            const maxValue = _.max(fieldsData)
            data = faker.number.int({min: maxValue+1})
        } else if (condition === '<') {
            const fields =  _.isArray(conditions["<"]) ? conditions["<"] : Array.from(conditions["<"])
            const fieldsData = _.map(fields, (field) => event[field])
            const minValue = _.min(fieldsData)
            data = faker.number.int({min: 0, max: minValue})
        } else if (condition === '>') {
            const fields =  _.isArray(conditions[">"]) ? conditions[">"] : Array.from(conditions[">"])
            const fieldsData = _.map(fields, (field) => event[field])
            const maxValue = _.max(fieldsData)
            data = faker.number.int({min: maxValue})
        } 
    }
    return _.toNumber(data);
}

const applyStringConditions = (conditions, event) => {
    for (const condition in conditions) {
        if (condition === 'faker') {
            return _.toString(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 

        // date range
    }
}

const applyArrayConditions = (conditions, event) => {
    for (const condition in conditions) {
        if (condition === 'faker') {
            return _.toString(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 
    }
    // Occurences of the fileds
}

const applyBooleanConditions = (conditions, event) => {
    for (const condition in conditions) {
        if (condition === 'faker') {
            return _.toString(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 
    }

    // occurence of the true, false
}

const applyConditions = (conditions, event) => {
    for (const field in conditions) {
        const data = _.get(event, field)
        const fieldConditions = _.get(conditions, field)
        // console.log(field, fieldConditions)
        if (_.isNumber(data)) {
            const data = applyNumberConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isString(data)) {
            const data = applyStringConditions(fieldConditions, event)
            _.set(event, field, data)
        }


    }
    return event;
}


const applyDenorm = () => {

// apply denorm

}


const start = async (templatePath, count = 10, outputPath) => {
    try {
        const writeStream = fs.createWriteStream("../output/vsk/student-attendance.json")
        let template = await fs.readJson(templatePath);
        const schema = template?.template?.schema;
        const conditions = template?.template?.conditions;
        for (let index = 0; index < count; index++) {
            let event = generate(schema)
            if (!_.isEmpty(conditions)) {
                event = applyConditions(conditions, event)
            }
            writeStream.write(JSON.stringify(event)+'\n')
        }
        writeStream.close()
    } catch (error) {
        console.log(`Error while generating the events`, error)
    }
}


start("/Users/harishkumargangula/Documents/GitHub/obsrv-samples/templates/vsk/student-attendance.json")
