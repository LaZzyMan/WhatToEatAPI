import pymongo
from flask import jsonify

# return a collection
def get_coll():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.WhatToEat
    user = db.User
    return user

class UserAddHistory(object):

    def __init__(self, json):
        self.userID = json['userID'] #string
        self.date = json['date']  #string
        self.restaurant = json['restaurant']  #string
        self.recipe = json['recipe']  #array
        self.health = json['health']  #array

    def addhistory(self):
        coll = get_coll()
        result = coll.update_one({"userID": self.userID}, {"$push": {"history": {"date": self.date, "restaurant": self.restaurant, "recipe": self.recipe, "health": self.health}}})
        if not result.matched_count:
            return "False"
        else:
            return "True"


class UserDeleteHistory(object):

    def __init__(self, json):
        self.userID = json['userID'] #string

    def deletehistory(self):
        coll = get_coll()
        result = coll.update_one({"userID": self.userID}, {"$unset": {"history": 1}})
        if not result.matched_count:
            return "False"
        else:
            return "True"

class History(object):

    def __init__(self, json):
        self.userID = json['userID'] #string

    def history(self):
        coll = get_coll()
        user = coll.find_one({"userID": self.userID})
        if not user:
            return "Have no this account!"
        #db.students.find({"parents":{"$exists":true}}).pretty();
        his = coll.find_one({"userID": self.userID, "history": {"$exists": True}})
        if not his:
            return "Have no history!"
        else:
            return jsonify(user['history'])