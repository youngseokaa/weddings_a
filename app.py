from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient



app = Flask(__name__)


client = MongoClient('mongodb+srv://youngseok:dhdudtjr11!@cluster0.jactwgi.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/myPage')
def signUp():
    return render_template('myPage.html')


@app.route('/signUp')
def signIn():
    return render_template('signUp.html')


@app.route('/edit')
def edit():
    return render_template('weddingEdit.html')

@app.route("/edit/cancel", methods=["POST"])
def weddingCancel():
    num_receive = request.form['num_give']
    db.wedding.delete_one({'num':num_receive})
    return jsonify({'msg':'취소 완료!'})
@app.route('/modify')
def modify():
    return render_template('weddingModify.html')

@app.route('/write', methods=["GET"])
def write():
    return render_template('weddingWrite.html')

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

