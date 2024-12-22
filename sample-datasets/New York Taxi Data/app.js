const request = require('request')
const csv = require('csvtojson')
const fs = require('fs')
const csvSplitStream = require('csv-split-stream');
const _ = require('lodash');
const dayjs = require('dayjs');
const { v4: uuidv4 } = require('uuid')
const { faker } = require('@faker-js/faker');



// const readStream = fs.createReadStream("output-0.csv")
// const writeStream = fs.createWriteStream("output-0.json")



// const data = fs.readFileSync('output-0.json', 'utf-8')
// const parsed = JSON.parse(data)

// const chunks = _.chunk(parsed, 200);

// for (let index = 0; index < chunks.length; index++) {
//   fs.writeFileSync(`chunk-${index+1}.json`, JSON.stringify(chunks[index]))
// }

// readStream.pipe(csv({downstreamFormat: 'array'})).pipe(writeStream);


// return csvSplitStream.split(
//     readStream,
//     {
//       lineLimit: 1000000
//     },
//     (index) => fs.createWriteStream(`output-${index}.csv`)
//   )
//   .then(csvSplitResponse => {
//     console.log('csvSplitStream succeeded.', csvSplitResponse);
//     // outputs: {
//     //  "totalChunks": 350,
//     //  "options": {
//     //    "delimiter": "\n",
//     //    "lineLimit": "10000"
//     //  }
//     // }
//   }).catch(csvSplitError => {
//     console.log('csvSplitStream failed!', csvSplitError);
//   });


function getRandomDate(time) {
  const startDate = new Date('2023-02-21');
  const endDate = new Date('2024-03-13');
  const timeOfTrip = new Date(time)
  const timeDiff = endDate.getTime() - startDate.getTime();
  const randomTime = Math.random() * timeDiff;
  const randomDate = new Date(startDate.getTime() + randomTime);
  const randomHours = timeOfTrip.getHours();
  const randomMinutes = timeOfTrip.getMinutes();
  const randomSeconds = timeOfTrip.getSeconds();
  const randomMilliseconds = timeOfTrip.getMilliseconds();
  randomDate.setHours(randomHours, randomMinutes, randomSeconds, randomMilliseconds);
  return dayjs(randomDate).format('YYYY-MM-DD HH:mm:ss')
}


// for (let index = 1; index <= 1; index++) {
//   const data = fs.readFileSync(`chunk-${index}.json`, 'utf-8')
//   let parsed = JSON.parse(data);
//   parsed = _.map(parsed, item => {
//     return {...item, ...{tpep_pickup_datetime: getRandomDate(item.tpep_pickup_datetime), tpep_dropoff_datetime: getRandomDate(item.tpep_dropoff_datetime)}}
//   })
//   fs.writeFileSync(`chunk-${index}.json`, JSON.stringify(parsed))
// }


for (let index = 1; index <= 5000; index++) {
  const data = fs.readFileSync(`events/chunk-${index}.json`, 'utf-8')
  let parsed = JSON.parse(data);
  parsed = _.map(parsed, item => {
    let newItem = {
      "tripID": uuidv4(),
      "VendorID": item.VendorID.toString(),
      "tpep_pickup_datetime": item.tpep_pickup_datetime,
      "tpep_dropoff_datetime": item.tpep_dropoff_datetime,
      "passenger_count": item.passenger_count.toString(),
      "trip_distance": item.trip_distance.toString(),
      "RatecodeID": item.RatecodeID.toString(),
      "store_and_fwd_flag": item.store_and_fwd_flag,
      "PULocationID": item.PULocationID.toString(),
      "DOLocationID": item.DOLocationID.toString(),
      "payment_type": item.payment_type.toString(),
      "primary_passenger": {
        "email": faker.internet.email(),
        "mobile": faker.phone.number(),
      },
      "fare_details": {
        "fare_amount": parseInt(item.fare_details.fare_amount),
        "extra": parseFloat(item.fare_details.extra),
        "mta_tax": parseFloat(item.fare_details.mta_tax),
        "tip_amount": parseInt(item.fare_details.tip_amount),
        "tolls_amount": parseInt(item.fare_details.tolls_amount),
        "improvement_surcharge": parseFloat(item.fare_details.improvement_surcharge),
        "total_amount": parseInt(item.fare_details.total_amount),
        "congestion_surcharge": parseInt(item.fare_details.tip_amount / 5)
      }
    }
    return newItem;
  })
  fs.writeFileSync(`events/chunk-${index}.json`, JSON.stringify(parsed))
}
