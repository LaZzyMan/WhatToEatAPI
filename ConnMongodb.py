# -*- coding: UTF-8 -*-
from flask import Flask, make_response, request, jsonify, abort, send_from_directory, send_file
from flask_httpauth import HTTPBasicAuth
from forUserLogin import UserLogin
from forUsers import UserRegister, UserChangeInfo
from forAdministrators import UserAddHistory, UserDeleteHistory, History
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import random
import os
#from forConfirmEmail import SendMessage, IMessage

whatToEat = Flask(__name__)
auth = HTTPBasicAuth()
whatToEat.config['UPLOAD_FOLDER'] = 'static/'
whatToEat.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

@auth.get_password
def get_password(username):
    if username == 'xjy':
        return '20170724'
    return None
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access.'}), 403)

@whatToEat.route('/')
def hello_world():
    return "Enter OK"

@whatToEat.route('/api/v2.0/test')
@auth.login_required
def test():
    return "OK"

@whatToEat.route('/api/v2.0/register', methods = ['PUT'])
@auth.login_required
def register():
    if not request.json:
        abort(404)
    user = UserRegister(request.json)
    re = user.register()
    return jsonify({'result':re})

@whatToEat.route('/api/v2.0/login', methods = ['PUT'])
@auth.login_required
def login():
    if not request.json:
        abort(404)
    user = UserLogin(request.json)
    re = user.login()
    if re == 'True':
        result = {}
        result['result'] = re
        result['user'] = user.getUser()
        return jsonify({'result': re, 'user': user.getUser()})
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/changeinfo', methods = ['PUT'])
@auth.login_required
def changeinfo():
    if not request.json:
        abort(404)
    user = UserChangeInfo(request.json)
    re = user.changeinfo()
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/addhistory', methods = ['PUT'])
@auth.login_required
def addhistory():
    if not request.json:
        abort(404)
    user = UserAddHistory(request.json)
    re = user.addhistory()
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/deletehistory', methods = ['PUT'])
@auth.login_required
def deletehistory():
    if not request.json:
        abort(404)
    user = UserDeleteHistory(request.json)
    re = user.deletehistory()
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/history', methods = ['PUT'])
@auth.login_required
def history():
    if not request.json:
        abort(404)
    user = History(request.json)
    re = user.history()
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/uploadimage', methods = ['POST'])
def uploadimage():
    upload_file = request.files['headimage']
    if upload_file:
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(whatToEat.root_path, whatToEat.config['UPLOAD_FOLDER'], filename))
        return jsonify({'result':1})
    else:
        return jsonify({'result':0})

@whatToEat.route('/api/v2.0/downloadimage', methods = ['POST'])
@auth.login_required
def downimage():
    userId = request.json['userID']
    return send_from_directory(whatToEat.static_folder, userId+'.jpg')

@whatToEat.route('/api/v2.0/download/<filename>', methods = ['GET'])
def downloadimage(filename):
    return send_from_directory(whatToEat.static_folder, filename)

@whatToEat.route('/api/v2.0/sendmessage', methods = ['PUT'])
@auth.login_required
def send():
    if not request.json:
        abort(404)
    user = SendMessage(request.json)
    re = user.sendmessage()
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/ensureemail', methods = ['PUT'])
@auth.login_required
def ensure():
    if not request.json:
        abort(404)
    user = IMessage(request.json)
    re = user.ensuremessage()
    return jsonify({'result': re})

@whatToEat.route('/api/v2.0/recommand', methods=['PUT'])
def recommand():
    json = request.json
    client = MongoClient()
    restaurantDB = client.WhatToEat.Restaurant
    print ("成功连接到数据库")
    restaurantToChoose = json['restaurants']
    energy = json['energy']
    restaurants = []
    i = 0
    for restaurant in restaurantToChoose:
        result = list(restaurantDB.find({"name": restaurant['name']}))
        if len(result) != 0:
            result[0]['distance'] = restaurant['distance']
            del result[0]['_id']
            result[0]['index'] = i
            restaurants.append(result[0])
    print ("餐厅数据读取完成")

    randomPart = []
    distanceTmp = []
    energyTmp = []
    for restaurant in restaurants:
        randomPart.append(random.random())
        distanceTmp.append(restaurant['distance'])
        energyTmp.append(abs(restaurant['hot'] - energy))
    distancePart = [(i - min(distanceTmp)) / (max(distanceTmp) - min(distanceTmp) + 0.01) for i in distanceTmp]
    energyPart = [(i - min(energyTmp)) / (max(energyTmp) - min(energyTmp) + 0.01) for i in energyTmp]
    for i in range(len(restaurants)):
        restaurants[i]['rate'] = randomPart[i] * 0.4 + distancePart[i] * 0.2 + energyPart[i] * 0.4
    restaurants.sort(key=lambda a: a['rate'])
    recommandRestaurant = {}
    i = 0
    for restaurant in restaurants:
        recommandRestaurant[str(i)] = restaurant
        i += 1
    print("餐厅推荐完成")
    print(len(restaurants))
    return jsonify(recommandRestaurant)

if __name__ == '__main__':
    whatToEat.run()

#login
#input: userID and password
#result: determined whether the userID and password are correct
#output: not exist/ password wrong/ true

#register
#input: userID, name, password, email, weight, height, gender, birthday, remind
#result: insert a collection to User Doc
#output: already exists/ didn't confirm/ true

#change informaiton
#input: userID, name, email, weight, height, gender, birthday, remind
#result: change the user(collection) of User Doc selected
#output: failed/ true

#delete history
#input: userID
#result: clear the history of the user(collection) selected in User Doc
#output: false/ true

#add history
#input: userID, date, restaurant, recipe, health
#recipe and health are both arrays within dictionaries
#example:
    #"recipe": [{"name": " A ", "hot": 123},{"name": " B " , "hot": 123},{"name": " C ", "hot": 123}]
    #"health": [{"distance": 1000}, {"step": 10000}, {"floors": 18}]
#result: add a history of the user(collection) selected in User Doc
#output: false/ true

#send random number to email
#input: userID
#send a random number to the user's email
#output: true

#comfirm the email
#input userID, confirmnumber
#determined whether the userID and confirmnumber are correct, if the confirmnuber is correct, the account passes validation and can login now
#output: false/ true

#recommand restaurant
#input example {"energy": 800,"restaurants": [{"name": "金马门国际美食百汇(珞喻路店)","distance": 450}]}
'''
output example {
    "0": {
        "address": "屯珞喻路87号君宜王朝大饭店5楼(近赛博数码广场)",
        "avgPrice": "156",
        "commentScore": {
            "environment": "9.0",
            "service": "8.9",
            "taste": "9.0"
        },
        "distance": 450,
        "hot": 672.9739130434783,
        "index": 0,
        "location": {
            "lat": 30.525540041914976,
            "lng": 114.35919024013658
        },
        "name": "金马门国际美食百汇(珞喻路店)",
        "rate": 0.26194263971441395,
        "recipe": [
            {
                "hot": 193,
                "name": " 三文鱼 "
            },
            {
                "hot": 183,
                "name": " 哈根达斯 "
            },
            {
                "hot": 97,
                "name": " 虾饺 "
            },
            {
                "hot": 287,
                "name": " 天妇罗 "
            },
            {
                "hot": 180,
                "name": " 生鱼片 "
            },
            {
                "hot": 196,
                "name": " 提拉米苏 "
            },
            {
                "hot": 145,
                "name": " 大蟹腿 "
            },
            {
                "hot": 180,
                "name": " 芝士蛋糕 "
            },
            {
                "hot": 225,
                "name": " 红酒煎鹅肝 "
            },
            {
                "hot": 212,
                "name": " 芒果布丁 "
            },
            {
                "hot": 266,
                "name": " 芝士焗扇贝 "
            },
            {
                "hot": 196,
                "name": " 牛排 "
            },
            {
                "hot": 133,
                "name": " 寿司 "
            },
            {
                "hot": 276,
                "name": " 烤生蚝 "
            },
            {
                "hot": 286,
                "name": " 酥皮汤 "
            },
            {
                "hot": 126,
                "name": " 焗蜗牛 "
            },
            {
                "hot": 299,
                "name": " 鹅肝 "
            },
            {
                "hot": 146,
                "name": " 卤甲鱼 "
            },
            {
                "hot": 212,
                "name": " 鳗鱼 "
            },
            {
                "hot": 265,
                "name": " 佛跳墙 "
            },
            {
                "hot": 217,
                "name": " 生蚝 "
            },
            {
                "hot": 297,
                "name": " 鲍鱼 "
            },
            {
                "hot": 220,
                "name": " 片皮鸭 "
            }
        ],
        "tel": "027-87687878",
        "type": "自助餐"
    }
}
'''
#upload image
#input data['headimage']
#ouput result:1/0

#downloadimage
#input userID
#ouput userID.jpg

