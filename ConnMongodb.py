# -*- coding: UTF-8 -*-
from flask import Flask, make_response, request, jsonify, abort, send_from_directory
from flask_httpauth import HTTPBasicAuth
from forUserLogin import UserLogin
from forUsers import UserRegister, UserChangeInfo
from forAdministrators import UserAddHistory, UserDeleteHistory, History
from werkzeug.utils import secure_filename
import os
#from forConfirmEmail import SendMessage, IMessage

whatToEat = Flask(__name__)
auth = HTTPBasicAuth()
whatToEat.config['UPLOAD_FOLDER'] = '/'
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
