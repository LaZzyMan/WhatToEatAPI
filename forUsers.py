# -*- coding: UTF-8 -*-
import pymongo
from werkzeug.security import generate_password_hash
import random

# return a collection
def get_coll():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.WhatToEat
    user = db.User
    return user

class UserRegister(object):

    def __init__(self, json):
        self.userID = json['userID'] #string
        self.password = json['password'] #string
        self.name = json['name'] #string
        self.email = json['email'] #string
        self.gender = json['gender'] #double
        self.weight = json['weight'] #double
        self.height = json['height'] #double
        self.birthday = json['birthday'] #string
        self.remind = json['remind'] #double

    #def set_password(self, password):
        #self.pw_hash = generate_password_hash(password)

    #def check_password(self, password):
        #return check_password_hash(self.pw_hash, password)

    def register(self):
        coll = get_coll()
        user = coll.find_one({"userID": self.userID})
        if not user:
            self.pw_hash = generate_password_hash(self.password)
            newuser = {"name": self.name, "email": self.email, "userID": self.userID, "password": self.pw_hash,
                       "birthday": self.birthday, "gender": self.gender, "remind": self.remind, "weight": self.weight,
                       "height": self.height, "isconfirmed": 0, "confirmnumber": str(random.randint(1000,9999))}
            result = coll.insert_one(newuser)
            if not result.inserted_id:
                return "False"
            else:
                return "True"
        else:
            return "The account already exists!"

    def password_hash(selfs):
        se = '123456'
        pw_hash = generate_password_hash(se)
        return pw_hash

class UserChangeInfo(object):

    def __init__(self, json):
        self.userID = json['userID']  # string
        self.name = json['name']  # string
        self.email = json['email']  # string
        self.gender = json['gender']  # double
        self.weight = json['weight']  # double
        self.height = json['height']  # double
        self.birthday = json['birthday']  # string
        self.remind = json['remind']  # double

    def changeinfo(self):
        coll = get_coll()
        newuser = {"name": self.name, "email": self.email, "birthday": self.birthday, "gender": self.gender,
                   "remind": self.remind, "weight": self.weight, "height": self.height}
        result = coll.update_one({"userID": self.userID}, {"$set": newuser})
        if not result.matched_count:
            return "Failed to change the information!"
        else:
            return "True"


