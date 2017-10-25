import pymongo
from werkzeug.security import check_password_hash
from flask import jsonify

# return a collection
def get_coll():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.WhatToEat
    user = db.User
    return user

def get_restaurant():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.WhatToEat
    restaurant = db.Restaurant
    return restaurant

class UserLogin(object):

    def __init__(self, json):
        self.userID = json['userID'] #string
        self.password = json['password'] #string

    def login(self):
        coll = get_coll()
        user = coll.find_one({"userID": self.userID})
        if not user:
            return "This account does not exist!"
        elif user['isconfirmed'] == 0:
            return "This account has not confirmed!"
        elif check_password_hash(user['password'], self.password):
            return "True"
        else:
            return "The password is wrong"

    def getUser(self):
        coll = get_coll()
        rest = get_restaurant()
        user = coll.find_one({"userID": self.userID})
        user.pop('_id')
        for record in user['history']:
            rInfo = get_restaurant().find_one({"name": record['restaurant']})
            rInfo.pop('_id')
            record['restaurant'] = rInfo
        return user
