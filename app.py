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


<<<<<<< HEAD
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
=======
@app.route('/edit')
def edit():
    return render_template('weddingEdit.html')

@app.route("/edit/cancel", methods=["POST"])
def weddingCancel():
    num_receive = request.form['num_gives']
    db.wedding.delete_one({'num': int(num_receive)})
    return jsonify({'msg':'취소 완료!'})
@app.route('/modify')
def modify():
    return render_template('weddingModify.html')

@app.route('/write', methods=["GET"])
def write():
    return render_template('weddingWrite.html')

@app.route('/write/check', methods=["GET"])
def signUpGet():
    weddinglist = list(db.wedding.find({}, {'_id': False}))
    return jsonify({'wedding': weddinglist})

@app.route('/write_invitation', methods=["POST"])
def write_invitation():
    wedding_list = list(db.wedding.find({}, {'_id': False}))
    num = len(wedding_list) + 1

    manName_receive = request.form['manName_give']
    girlName_receive = request.form['girlName_give']
    weddingDay_receive = request.form['weddingDay_give']
    weddingPlace_receive = request.form['weddingPlace_give']
    comment_receive = request.form['comment_give']
    manMom_receive = request.form['manMom_give']
    manDad_receive = request.form['manDad_give']
    girlMom_receive = request.form['girlMom_give']
    girlDad_receive = request.form['girlDad_give']
    manAccount_receive = request.form['manAccount_give']
    girlAccount_receive = request.form['girlAccount_give']

    doc = {
        'manName': manName_receive,
        'girlName': girlName_receive,
        'weddingDay': weddingDay_receive,
        'weddingPlace': weddingPlace_receive,
        'comment': comment_receive,
        'manMom': manMom_receive,
        'manDad': manDad_receive,
        'girlMom': girlMom_receive,
        'girlDad': girlDad_receive,
        'manAccount': manAccount_receive,
        'girlAccount': girlAccount_receive,
        'num':num
    }
    db.wedding.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})

>>>>>>> origin/wedding_num

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

