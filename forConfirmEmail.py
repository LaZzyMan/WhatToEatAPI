# -*- coding: UTF-8 -*-
import pymongo
from flask import Flask
from flask.ext.mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '598122401@qq.com'
app.config['MAIL_PASSWORD'] = 'dlcbuetnjnzkbbfe'
app.config['MAIL_DEBUG'] = True

# return a collection
def get_coll():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.WhatToEat
    user = db.User
    return user

class SendMessage(object):

    def __init__(self, json):
        self.userID = json['userID']

    def sendmessage(self):
        coll = get_coll()
        result = coll.find_one({"userID": self.userID})
        code = result['confirmnumber']
        address = result['email']
        mail = Mail(app)
        msg = Message('What to Eat Tonight', sender='598122401@qq.com', recipients=[address])
        msg.body = "Hello, dear friend!\nYour verification code is : " + code +"\nThanks for your support!"
        with app.app_context():
            mail.send(msg)
        return "True"

class IMessage(object):

    def __init__(self, json):
        self.userID = json['userID']
        self.confirmnumber = json['confirmnumber']  # string

    def ensuremessage(self):
        coll = get_coll()
        user = coll.find_one({"userID": self.userID})
        if not user:
            return "This account does not exist!"
        elif(user['confirmnumber'] == self.confirmnumber):
            coll.update_one({"userID": self.userID}, {"$set": {"isconfirmed": 1}})
            return "True"
        else:
            return "The number is wrong!"