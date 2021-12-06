from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)

db = client.dfindr

products = db.products
users = db.users

app = Flask(__name__)

app.secret_key = '9a5c0aaf287745d3b21bb5a22e6dah0e9c8fbr3bc39e34474f2f400f57'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def rlogin():
    if request.method=='GET':
        session['username']=request.form['username']
        return render_template('index.html')
    elif request.method=='POST':
        user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
        }
        user = users.insert_one(user)
        session['username']=request.form['username']
        print(user)
        user_obj = users.find_one({'username': session['username']})
        return render_template('index.html')

@app.route('/index')
def index():
    user_obj = users.find_one({'username': session['username']})
    return render_template('index.html', user_obj=user_obj, user=user_obj)

@app.route('/findr')
def findr():
    user_obj = users.find_one({'username': session['username']})
    return render_template('findr.html', user_obj=user_obj, user=user_obj)

@app.route('/iceland')
def iceland():
    return render_template('iceland.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)