from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient



app = Flask(__name__)


client = MongoClient('mongodb+srv://youngseok:dhdudtjr11!@cluster0.jactwgi.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

db = client.dbsparta

SECRET_KEY = 'SPARTA'

import jwt

import datetime

import hashlib


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)



@app.route('/register')
def join():
    return render_template('register.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    phone_receive = request.form['phone_give']
    email_receive = request.form['email_give']

    if id_receive == "":
        return jsonify({'msg':'아이디를 입력하세요'})

    if pw_receive == "":
        return jsonify({'msg': '비밀번호를 입력하세요'})

    if phone_receive == "":
        return jsonify({'msg': '핸드폰 번호를 입력하세요'})

    if email_receive == "":
        return jsonify({'msg': 'e_mail를 입력하세요'})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one(
    {'id': id_receive, 'pw': pw_hash, 'phone': phone_receive, 'email': email_receive})

    return jsonify({'result': 'success'})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    print(id_receive, pw_receive)

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

