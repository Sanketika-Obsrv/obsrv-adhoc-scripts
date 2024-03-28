const request = require('request')
const csv = require('csvtojson')
const fs = require('fs')
const csvSplitStream = require('csv-split-stream');
const _ = require('lodash');
const {v4: uuidv4} = require('uuid')



// const readStream = fs.createReadStream("output-0.csv")
// const writeStream = fs.createWriteStream("output-0.json")

// readStream.pipe(csv()).pipe(writeStream);

// const data = fs.readFileSync('output-0.json', 'utf-8')
// const parsed = JSON.parse(data)

// const chunks = _.chunk(parsed, 990);

// for (let index = 0; index < chunks.length; index++) {
//   fs.writeFileSync(`chunk-${index+1}.json`, JSON.stringify(chunks[index]))
// }


// for (let index = 1; index < 250; index++) {
//   const data = fs.readFileSync(`chunk-${index}.json`, 'utf-8')
//   const parsed = JSON.parse(data);
//   const last = parsed[989]
//   _.times(10, () => {
//     parsed.push(last)
//   })
//   fs.writeFileSync(`chunk-${index}.json`, JSON.stringify(parsed))
// }

// for (let index = 251; index <= 500; index++) { 
//   const data = fs.readFileSync(`chunk-${index}.json`, 'utf-8')
//   let parsed = JSON.parse(data);
//   let a = 0;
//   parsed = _.map(parsed, p => {
//     a++;
//     if(a <= 20) {
//       return {...p, ...{price:  parseInt(p.price)}}
//     } else {
//       return p
//     }
//   })
//   fs.writeFileSync(`chunk-${index}.json`, JSON.stringify(parsed))
// }


const getRandomTimeInSameDate = () => {
  const currentDate = new Date();

  // Generate random hours, minutes, seconds, and milliseconds
  const randomHours = Math.floor(Math.random() * 24);
  const randomMinutes = Math.floor(Math.random() * 60);
  const randomSeconds = Math.floor(Math.random() * 60);
  const randomMilliseconds = Math.floor(Math.random() * 1000);

  // Set the generated time to the current date
  currentDate.setHours(randomHours, randomMinutes, randomSeconds, randomMilliseconds);

  return currentDate;
}

function getRandomDate() {
  const startDate = new Date('2024-02-21');
const endDate = new Date('2024-03-15');
  const timeDiff = endDate.getTime() - startDate.getTime();
  const randomTime = Math.random() * timeDiff;
  const randomDate = new Date(startDate.getTime() + randomTime);
  return randomDate.toISOString().slice(0, 10);
}


for (let index = 501; index <= 1000; index++) {
  const data = fs.readFileSync(`chunk-${index}.json`, 'utf-8')
  let parsed = JSON.parse(data);
  parsed = _.map(parsed, item => {
    return {...item, ...{time: getRandomDate(), id: `{${uuidv4()}}`}}
  })
  fs.writeFileSync(`chunk-${index}.json`, JSON.stringify(parsed))
}

 
// return csvSplitStream.split(
//     readStream,
//     {
//       lineLimit: 1000000
//     },
//     (index) => fs.createWriteStream(`output-${index}.csv`)
//   )
//   .then(csvSplitResponse => {
//     console.log('csvSplitStream succeeded.', csvSplitResponse);
    // outputs: {
    //  "totalChunks": 350,
    //  "options": {
    //    "delimiter": "\n",
    //    "lineLimit": "10000"
    //  }
    // }
  // }).catch(csvSplitError => {
  //   console.log('csvSplitStream failed!', csvSplitError);
  // });