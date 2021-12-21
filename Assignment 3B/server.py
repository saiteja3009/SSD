from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.wrappers import response
app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Root1234@localhost:3306/ssddb"
app.config['SESSION_TYPE'] = "sqlalchemy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
cur_session = Session(app)
user_session = {}
chef_session = {}

'''classes are the tables required to store the data in the db'''


class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Menu(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    full_plate_price = db.Column(db.Float, nullable=True)
    half_plate_price = db.Column(db.Float, nullable=True)

    def __init__(self, item_id, half_plate_price, full_plate_price):
        self.item_id = item_id
        self.full_plate_price = full_plate_price
        self.half_plate_price = half_plate_price


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    total_amount = db.Column(db.Integer, nullable=False)
    tip_percent = db.Column(db.Float, nullable=False)
    discount_val = db.Column(db.Float, nullable=False)
    total_bill = db.Column(db.Float, nullable=False)

    def __init__(self, total_amount, tip_percent, discount_value, total_bill):
        self.username = user_session['username']
        self.total_amount = total_amount
        self.discount_val = discount_value
        self.tip_percent = tip_percent
        self.total_bill = total_bill


class Itemlist(db.Model):
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transaction.transaction_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'menu.item_id'), primary_key=True)
    type = db.Column(db.String(30), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, transaction_id, item_id, type, quantity):
        self.transaction_id = transaction_id
        self.item_id = item_id
        self.type = type
        self.quantity = quantity


''' The following are the required REST api calls for different functions'''


@app.route("/signup", methods=['POST'])
def signup():
    req = request.get_json()
    user = User.query.get(req['username'])
    if(user != None):
        return "Username already exists"
    else:
        usr = User(req['username'], req['password'], req['role'])
        db.session.add(usr)
        db.session.commit()
        return "Successfully Added to db"


@app.route("/login", methods=['POST'])
def login():
    req = request.get_json()
    user = User.query.get(req['username'])
    if(user == None):
        return "User doesn't exists"
    else:
        if user_session.get('username') != None:
            if req['username'] == user_session['username']:
                return "User already logged in"
            else:
                return "Another user already logged in"
        if req['password'] != user.password:
            return "Wrong Credentials"
        user_session['username'] = req['username']
        user_session['role'] = user.role
        return "Logged in Succesful"


@app.route("/logout", methods=['GET'])
def logout():
    if(user_session.get('username') == None):
        return "No user logged in"
    else:
        user_session.pop('username')
        return "Successfully logged out"


@app.route("/getmenu", methods=['GET'])
def menu():
    data = Menu.query.all()
    returnValue = {}
    if len(data) == 0:
        return "No Entries have been added yet"
    for menu in data:
        returnValue[menu.item_id] = {
            "half_plate_price": menu.half_plate_price, "full_plate_price": menu.full_plate_price}
    return jsonify(returnValue)


'''Get is to send the info and POST is to get the info from the customer'''


@app.route("/addmenu", methods=['POST'])
def addmenu():
    req = request.get_json()
    if(user_session['role'] != "chef"):
        return "You do not have access to add to menu"
    item = Menu.query.get(req['item_id'])
    if(item != None):
        return "Item already exists"
    else:
        usr = Menu(req['item_id'], req['half_plate_price'],
                   req['full_plate_price'])
        db.session.add(usr)
        db.session.commit()
        return "Successfully Added to Menu"


@app.route("/transaction", methods=['POST'])
def transaction():
    req = request.get_json()
    usr = Transaction(req['total_amount'], req['tip_percent'],
                      req['discount_val'], req['total_bill'])
    db.session.add(usr)
    db.session.commit()
    return str(usr.transaction_id)


@app.route("/itemlist", methods=['POST'])
def item_list():
    req = request.get_json()
    transactionid = req['transaction_id']
    items_list = req['items_list']
    for i in items_list:
        itemListObj = Itemlist(
            transaction_id=transactionid,
            item_id=i['item_id'],
            type=i['type'],
            quantity=i['quantity']
        )
        db.session.add(itemListObj)

    db.session.commit()
    return "Order Summary added successfully"


@app.route("/transac", methods=['GET'])
def get_trans():
    username = user_session['username']
    data = Transaction.query.filter_by(username=username)
    returnValue = {}
    j = 0
    for i in data:
        returnValue[j] = {"transaction_id": i.transaction_id}
        j += 1
        #returnValue[tx.transaction_id] = {"total_bill": tx.total_bill}
    return jsonify(returnValue)


@app.route("/transspe", methods=['POST'])
def post():
    req = request.get_json()
    transaction_id = req['transaction_id']
    transaction_summary = Transaction.query.filter_by(
        transaction_id=transaction_id).first()
    itemList = Itemlist.query.filter_by(transaction_id=transaction_id)
    order = {}
    for i in itemList:
        order[i.item_id] = [i.type, i.quantity]
        # if i.type=="Half":
        #     order[i.item_id]=i.quantity
        # else:
        #     order[i.item_id][1]=i.quantity

    returnValue = {}
    returnValue['order'] = order
    returnValue['total_amount'] = transaction_summary.total_amount
    returnValue['discount_val'] = transaction_summary.discount_val
    returnValue['total_bill'] = transaction_summary.total_bill
    returnValue['tip_percent'] = transaction_summary.tip_percent
    return jsonify(returnValue)


'''port at which the server runs is 8000'''

if __name__ == '__main__':
    app.run(port=8000, debug=True)
