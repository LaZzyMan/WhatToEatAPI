import json
import requests
from pymongo import MongoClient
db = MongoClient().WhatToEat.Restaurant
restaurants = db.find({})
for restaurant in restaurants:
    if restaurant['location'] == 0:
        restaurant['location'] = {"lat": 0, "lng": 0}
        db.save(restaurant)
    else:
        continue
    if 'location' in restaurant.keys():
        if restaurant['location'] != 0:
            continue
    else:
        restaurant['location'] = 0
        db.save(restaurant)
        continue
    url = "http://api.map.baidu.com/geocoder/v2/"
    querystring = {"address": restaurant['address'], "output": "json", "ak": "iQzNc1AEBVFXyzU7w7SQP5HSa01GH30k",
                   "ret_coordtype": "gcj02ll", "city": "\"武汉市\""}
    headers = {
        'cache-control': "no-cache",
        'postman-token': "f1bb1e5a-bc66-029b-04d4-c0fb2e036856"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)['result']
        restaurant['location'] = result['location']
        db.save(restaurant)
        print(restaurant['name'])
    except:
        continue

print('Finished!')
