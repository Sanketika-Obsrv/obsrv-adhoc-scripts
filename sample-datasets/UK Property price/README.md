
# UK  Property price

The data.zip contains 500 files each having 990 events

```javascript 
{
  "id": "{FCB2F40C-D96A-4130-B75A-CCAD3A756A77}",
  "price": "69750",
  "time": "2023-10-12",
  "postcode": "PE38 0DH",
  "property_type": "D",
  "new_old": "Y",
  "duration": "F",
  "primary_address": "20",
  "secondary_address": "",
  "street": "BEECHEY CLOSE",
  "locality": "DENVER",
  "town_city": "DOWNHAM MARKET",
  "district": "KING'S LYNN AND WEST NORFOLK",
  "county": "NORFOLK",
  "ppd_category_type": "A",
  "record_status": "A"
}
```


### Following Transformations needs to add as JSONAta expressions



1. property_type

```javascript

$lookup({
 "D" : "Detached",
 "S" : "Semi-Detached",
 "T" : "Terraced",
 "F" : "Flats/Maisonettes",
 "O" :"Other"
}, property_type)

```


2. new_old
```javascript

$uppercase($lookup({
"Y" : "newly built", 
"N" : "established building"
}, new_old))
```

3. duration

``` javascript

$lookup({
"F" : "Freehold", "L" :"Leasehold"
}, duration)

```

4. ppd_category_type

``` javascript

$lookup({
"A":"Standard Price Paid entry",
"B ":"Additional Price Paid entry"
}, ppd_category_type)

```

5. record_status

```javascript

$lookup({
"A":"Addition",
"C": "Change",
"D": "Delete"
}, record_status)

```

Refer: https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid
