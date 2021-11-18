"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS

from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user/<int:id>', methods=['GET'])
def getuser_byId(id):
    user= User.get_byid(id) 

    if user:
        return jsonify(user.to_dict()),200
    
    return jsonify({'error':'User not found'}), 404


@app.route('/user/<int:id>/task', methods=['GET'])
def get_usertasks(id):
    user= User.get_byid(id) 

    if user:
        tasks= Task.get_byuser(id)
        if tasks:
            all_tasks= [task.to_dict() for task in tasks]
            return jsonify(all_tasks), 200

      
        
        

    return jsonify({'error':'User not found'}), 404


@app.route('/user/<int:id>/task', methods=['POST'])
def create_usertask(id):
    user= User.get_byid(id) 
    text= request.json.get('text',None) #En Postman tendríamos que indicar text en el body
    if user and text:
        task=Task(text=text, done=False, user_id=id)
        task.create()
        return jsonify(task.to_dict()), 201
    

    return jsonify({'error':'Task not found'}), 404


@app.route('/user/<int:id>', methods=['DELETE'])
def deleteuser(id):
    user= User.get_byid(id) 

    if user:
        user= user.delete()
        return jsonify(user.to_dict()), 200
    
    return jsonify({'error':'User not found'}), 404


@app.route('/user', methods=['GET'])
def get_users():

    users= User.get_all()
    all_users = [user.to_dict() for user in users] #Pasamos los elementos de la lista a diccionarios

    return jsonify(all_users), 200


@app.route('/user', methods=['POST'])
def create_user():

    newuser= request.json.get('user', None)

    if not newuser:
        return jsonify({'error':'Missing data'}),400

    user= User(name=newuser,is_active=True)
    
    user_created= user.create()
    return jsonify(user_created.to_dict()),201


@app.route('/user/<int:id>/task/<int:id_task>', methods=['DELETE'])
def deletetask_user(id,id_task):
    user= User.get_byid(id) 

    if user:
        task= Task.gettask_id(id_task)
        
        if task:
            task=task.delete()
            return jsonify(task.to_dict()), 200
        
        return jsonify({'error':'Task not found'}), 404

    return jsonify({'error':'User not found'}), 404
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
