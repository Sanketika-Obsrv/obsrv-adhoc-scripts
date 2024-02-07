const fs = require('fs');
const readline = require('readline');
const dayjs = require('dayjs');
const _ = require('lodash');

const inputFilePath = './events.json';
const fileStream = fs.createReadStream(inputFilePath);
const readLineInterface = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

const getRandomDate = (record) => {
    const ets = _.get(record, 'ets');
    const minutes = _.random(0, 600)
    return dayjs(ets).add(1, 'day').startOf('day').add(minutes, 'minutes').valueOf()
}

const initParser = (fileWriter) => {
    readLineInterface.on('line', (line) => {
        try {
            const record = JSON.parse(line);
            const ets = getRandomDate(record)
            fileWriter({ ...record, ets  });
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    });
}

const fileWriterCloure = (filePath) => (data) => {
    const modifiedData = typeof data === "string" ? data : JSON.stringify(data);
    fs.writeFileSync(filePath, modifiedData + '\n', { flag: 'a' });
}

const fileWriter = fileWriterCloure("./output.json")
initParser(fileWriter);