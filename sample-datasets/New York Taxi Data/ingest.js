const axios = require('axios')
const { v4: uuidv4 } = require('uuid');
const fs = require('fs')
const axiosRetry = require('axios-retry').default;;

axiosRetry(axios, {
  retries: 10, // number of retries
  retryDelay: (retryCount) => {
    console.log(`retry attempt: ${retryCount}`);
    return retryCount * 2000; // time interval between retries
  }
});

function randomIntFromInterval(min, max) { // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min)
}

const delay = () => {
  const delayIn = randomIntFromInterval(6000, 20000)
  console.log(`After delay of ${delayIn} ms`)
  return new Promise(resolve => setTimeout(() => { resolve() }, delayIn))
}

const ingest = async () => {
  for (let index = 2; index <= 5; index++) {
    const data = {
      "data": {
        "id": uuidv4(),
        "events": []
      }
    }
    const events = fs.readFileSync(`chunk-${index}.json`, 'utf-8')
    data.data.events = JSON.parse(events);
    console.log(`start chunk ${index}`)
    let config = {
      method: 'post',
      maxBodyLength: Infinity,
      url: 'http://localhost:6000/data/v1/in/new-york-taxi-data',
      headers: {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
      },
      data: JSON.stringify(data)
    };
    await axios.request(config)
    console.log(`completed chunk ${index}`)
    await delay()

  }
}

ingest().then().catch(er => console.log(er))
