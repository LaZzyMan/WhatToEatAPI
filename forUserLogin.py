import pymongo
from werkzeug.security import check_password_hash

# return a collection
def get_coll():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.WhatToEat
    user = db.User
    return user

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
