const axios = require('axios')
const { v4: uuidv4 } = require('uuid');
const fs = require('fs')
const axiosRetry = require('axios-retry').default;;

axiosRetry(axios, {
    retries: 20, // number of retries
    retryDelay: (retryCount) => {
        console.log(`retry attempt: ${retryCount}`);
        return retryCount * 2000; // time interval between retries
    }
});

function randomIntFromInterval(min, max) { // min and max included 
  return Math.floor(Math.random() * (max - min + 1) + min)
}

const delay = () => {
  const delayIn = randomIntFromInterval(10000, 30000)
    console.log(`After delay of ${delayIn} ms`)
    return new Promise(resolve => setTimeout(() => { resolve()}, delayIn))
}

const ingest = async () => {
    for (let index = 501; index < 553; index++) {
        const data = {
            "data": {
              "id": uuidv4(),
              "events":[]}
        }
        const events = fs.readFileSync(`chunk-${index}.json`, 'utf-8')
        data.data.events = JSON.parse(events);
        console.log(`Started ${index}`)
        let config = {
            method: 'post',
            maxBodyLength: Infinity,
            url: 'http://localhost:6000/data/v1/in/uk-property-price',
            headers: { 
              'authority': '18.189.87.205.sslip.io', 
              'accept': 'application/json, text/plain, */*', 
              'accept-language': 'en-GB,en;q=0.9', 
              'cache-control': 'no-store', 
              'content-type': 'application/json', 
              'cookie': 'connect.sid=s%3AyVyygL060Sdhs5OPPqWZvgJf-6RZVYbl.KanNBbSCs2dutMy%2B3b0D731BNxBkUjd5476Jwn90BSE; session=.eJw1kMuSmkAARX8l1ess6BfQ7kSNMjoSNXHQVMrqpyCGRzcoOjX_HlJJlmdxb5067-BkrHYZGBl-dfozOOUKjIAhHkRIiZCG1IfSCEQpDRnTyhOeURjJEHrcEIEN96UHhUZMEywwhlgbxQKkZYA86HtKsiBQHAUY-9z4GmnDiZRQSEwDxHyKhik2yDNsOAyoQAxSDwwindP2rw0a8FpJftUD6HKginft4PwOPrVg9AMkusnHuCiLR3vWs-IxhXP-zKbL-b6N1snKwrdC7IJdnG3HbjndMUbE5Nu0ecZ9lY5bk6vmqFep9kWYdPluQlLW33U3IZV6pqY8HrJV_mv9hW3j2-zs0ucmqKPikSgdqvusrvVmEcYQH1ywcOOcrtlCyMsq79W9opiTfbTNquPL4WszH36jMqPRa5rUTvZxQ9ZWiNnzewTdta_mgROGrG7Z0l7e4nNo637zsJsdvI0XRcbKLpZ7gWI2EaZPcUtV2Q0twM-Pf0FOta1uudJ2yFQJZ2__S51cy9s_8WbJ6wuBLaqhviwXsXXNpovhVRHXJIcj-PgNEH6pKA.ZcCEZg.iK5S8uKKFdKUS1_6ML5bV1_kfY0', 
              'origin': 'https://18.189.87.205.sslip.io', 
              'pragma': 'no-store', 
              'referer': 'https://18.189.87.205.sslip.io/console/datasets/addEvents/uk-property-price', 
              'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"', 
              'sec-ch-ua-mobile': '?0', 
              'sec-ch-ua-platform': '"macOS"', 
              'sec-fetch-dest': 'empty', 
              'sec-fetch-mode': 'cors', 
              'sec-fetch-site': 'same-origin', 
              'sec-gpc': '1', 
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            },
            data : JSON.stringify(data)
          };
          
        
        await axios.request(config)
        console.log(`Completed ${index}`)
        await delay()
    }
}

ingest().then().catch(er => console.log(er))
