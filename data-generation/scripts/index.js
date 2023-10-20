
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

        if (condition === 'occurences' && conditions?.occurences?.data) { 
            let occurencesData = conditions?.occurences?.data
            occurencesData = _.map(occurencesData, (d) => {
                return ({ weight: d?.weight/ 10, value: d?.value })
             })
             data = faker.helpers.weightedArrayElement(occurencesData);
        }
    }
    return _.toNumber(data);
}

const applyStringConditions = (conditions, event) => {
    let data;
    for (const condition in conditions) {
        if (condition === 'faker') {
            return _.toString(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 

        if(condition == 'format') {
            const type = conditions?.format?.type;
            if(type && _.toLower(type) === 'date') {
                const from = conditions?.format?.range?.from || new Date(); // today
                const to = conditions?.format?.range?.to || new Date(new Date().getTime() + 24 * 60 * 60 * 1000); // tomoor
                data = faker.date.between({from, to}) 
            }
        }
        if (condition === 'occurences' && conditions?.occurences?.data) { 
            let occurencesData = conditions?.occurences?.data
            occurencesData = _.map(occurencesData, (d) => {
                return ({ weight: d?.weight/ 10, value: d?.value })
             })
             data = faker.helpers.weightedArrayElement(occurencesData);
        }
    }
    
    return data;
}

const applyArrayConditions = (conditions, event) => {
    for (const condition in conditions) {
        if (condition === 'faker') {
            return _.toString(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 
    }
}

const applyBooleanConditions = (conditions, event) => {
    let data;
    for (const condition in conditions) {
        if (condition === 'faker') {
            return _.toString(faker.helpers.fake(`{{${conditions.faker}}}`))
        } 
        if (condition === 'occurences' && conditions?.occurences?.data) { 
            let occurencesData = conditions?.occurences?.data
            occurencesData = _.map(occurencesData, (d) => {
                return ({ weight: d?.weight/ 10, value: d?.value })
             })
             data = faker.helpers.weightedArrayElement(occurencesData);
        }
    }
    return data;
}

const applyConditions = (conditions, event) => {
    for (const field in conditions) {
        const fieldDate = _.get(event, field)
        const fieldConditions = _.get(conditions, field)
        if (_.isNumber(fieldDate)) {
            const data = applyNumberConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isString(fieldDate)) {
            const data = applyStringConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isArray(fieldDate)) {
            const data = applyArrayConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isBoolean(fieldDate)) {
            const data = applyBooleanConditions(fieldConditions, event)
            _.set(event, field, data)
        }


    }
    return event;
}


const applyDenorm = () => {

// apply denorm

}


const start = async (templatePath, count = 100, outputPath) => {
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


start("/Users/harishkumargangula/Documents/GitHub/obsrv-adhoc-scripts/data-generation/templates/vsk/student-attendance.json")
