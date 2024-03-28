
events.zip contains the files each with 1000 events

**taxi_zone_lookup.json**  is the master dataset with LocationId as data key.


**Sample event**

```javascript
{
  "tripID": "c606ab6e-0c1d-4e69-a8db-f0fc05fa9139",
  "VendorID": "1",
  "tpep_pickup_datetime": "2023-04-17 00:46:40",
  "tpep_dropoff_datetime": "2023-04-17 00:53:20",
  "passenger_count": "1",
  "trip_distance": "1.50",
  "RatecodeID": "1",
  "store_and_fwd_flag": "N",
  "PULocationID": "151",
  "DOLocationID": "239",
  "payment_type": "1",
  "primary_passenger": {
    "email": "Edd.Hodkiewicz@hotmail.com",
    "mobile": "1-535-298-9814 x3933"
  },
  "fare_details": {
    "fare_amount": "7",
    "extra": "0.5",
    "mta_tax": "0.5",
    "tip_amount": "1.65",
    "tolls_amount": "0",
    "improvement_surcharge": "0.3",
    "total_amount": "9.95",
    "congestion_surcharge": ""
  }
}
```

### Transformations

1. RateCodeID
```javascript

$lookup({
"1": "Standard rate",
"2": "JFK",
"3": "Newark",
"4": "Nassau or Westchester",
"5": "Negotiated fare",
"6": "Group ride"},
 RatecodeID)

```
2. payment_type
```javascript

$lookup({
"1" : "Credit card",
"2" : "Cash",
"3" : "No charge",
"4" : "Dispute,
"5" : "Unknown",
"6" " "Voided trip"},
 payment_type)

 ```

 ### Denorms

