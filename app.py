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

@app.route('/modify')
def modify():
    return render_template('weddingModify.html')

@app.route('/write')
def write():
    return render_template('weddingWrite.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

