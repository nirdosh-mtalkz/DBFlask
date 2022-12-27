from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['MONGO_URI'] = "mongodb://localhost:27017/data"

mongo = PyMongo(app)


@app.route('/add',methods=['POST'])
def add():
    name = request.json['name']
    pwd = request.json['pass']
    if name and pwd and request.method=="POST":
        id = mongo.db.emp.insert_one({'name':name,'pass':pwd})
        resp = "User added Succesfully"
        return jsonify(resp)

    else:
        return not_found()
    
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':"Not Found" + request.url
    }
    resp = jsonify(message)
    return resp

@app.route('/employee',methods=['GET'])
def show():
    users = mongo.db.emp.find()
    resp = dumps(users)
    return resp


@app.route('/emp/<id>',methods=['GET'])
def show_one(id):
    users = mongo.db.emp.find_one({'_id':ObjectId(id)})
    resp = dumps(users)
    return resp

if __name__ == "__main__":
    app.run()