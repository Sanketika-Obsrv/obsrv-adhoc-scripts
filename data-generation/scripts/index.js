
const fs = require('fs-extra');
const jsf = require('json-schema-faker');
const _ = require('lodash');
const { faker } = require('@faker-js/faker');
const prompts = require('prompts');
const path = require('path');

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
        const fieldData = _.get(event, field)
        const fieldConditions = _.get(conditions, field)
        if (_.isNumber(fieldData)) {
            const data = applyNumberConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isString(fieldData)) {
            const data = applyStringConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isArray(fieldData)) {
            const data = applyArrayConditions(fieldConditions, event)
            _.set(event, field, data)
        } else if(_.isBoolean(fieldData)) {
            const data = applyBooleanConditions(fieldConditions, event)
            _.set(event, field, data)
        }


    }
    return event;
}


const applyDenorm = (configs, event) => {
    let data = event
    for(const config of configs) {
        if(_.isObject(config.values[0])) {
            
            let pathObject = _.get(event, config?.path) || data;
            if(_.get(config, 'values[0].weight')) {
                let values = _.map(config.values, (value) => {
                    return ({...value, ...{ weight: value?.weight/ 10 }})
                 })
                pathObject = {...pathObject, ...faker.helpers.weightedArrayElement(values)}
            } else { 
                pathObject = {...pathObject, ..._.sample(config.values)}
            }
            data = config?.path ? _.set(data, config.path, pathObject) : pathObject
        } else {
            data = _.set(data, config.path, _.sample(config.values))   
        }
        // console.log(data)
    }
    return  data;

}


const start = async (templatePath, count = 1000, outputPath) => {
    try {
        const writeStream = fs.createWriteStream(outputPath)
        let template = await fs.readJson(templatePath);
        const schema = template?.template?.schema;
        const conditions = template?.template?.conditions;
        const denormConfig = template?.template?.denormConfig
        for (let index = 0; index < count; index++) {
            let event = generate(schema)
            if (!_.isEmpty(conditions)) {
                event = applyConditions(conditions, event)
            }
            if(!_.isEmpty(denormConfig)) {
                event = applyDenorm(denormConfig, event)
            }
            writeStream.write(JSON.stringify(event)+'\n')
        }
        writeStream.close()
    } catch (error) {
        console.log(`Error while generating the events`, error)
    }
}

const questions = [
    {
        type: 'select',
        name: 'template',
        message: 'Pick a template to generate events',
        choices: [
          { title: 'VSK', value: 'vsk' },
          { title: 'api monitoring', value: 'api-monitoring' }
        ],
        initial: 1
      },
      {
        type: 'number',
        name: 'count',
        message: 'How many events',
        initial: 1000,
        style: 'default',
        min: 1
      }
  ];
  
  (async () => {
    const response = await prompts(questions);
  
    const templatesDir = path.join(__dirname, '..' , 'templates', response.template)
    const files = await fs.readdir(templatesDir)
    for(const file of files) {
        const templatePath = path.join(templatesDir, file);
        const outputEventsPath = path.join(__dirname, '..' , 'output', response.template, file)
        await fs.ensureFile(outputEventsPath)
        start(templatePath, response?.count, outputEventsPath)
    }
  })();
  