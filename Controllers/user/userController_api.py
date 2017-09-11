from Flask_D01 import app
import crypt
import random, string
from flask import (request, jsonify, json, abort, make_response, Blueprint)
import re
from Models.user_model import User, UserModel

mod_api = Blueprint('api', __name__)

@mod_api.route('/user', methods=['POST'])
def create_user():
    if not request.json :
        return make_response(jsonify({'error': 'Not JSON request'}), 400) #not all requiered attributes in demand
    if not 'username' in request.json or not 'email' in request.json or not 'password' in request.json :
        return make_response(jsonify({'error': 'Bad parameters'}), 400) #not all requiered attributes in demand
    errors = validate_json_post(True) # get validation errors
    if(len(errors[0])):
        return make_response(jsonify({'error': 'Bad request', 'errors': errors}), 400)
    d_filter = {"username": "'" + request.json['username'] + "'"}
    model = UserModel()
    user = model.getUsers(d_filter)
    if len(user) != 0:
        errors[0]['username_error'] = "That username is already taken, please choose another"
        return make_response(jsonify({'error': 'Bad request', 'errors': errors}), 400)
    #prepare json data for insertion
    password = crypt.crypt(request.json['password'], getsalt())
    email = request.json['email']
    username = re.escape(request.json['username'])
    user = User(None, username, email, password)
    model = UserModel()
    user_ret = model.addUser(user,'json')
    return jsonify(user_ret), 201

@mod_api.route('/users', methods=['GET'])
def get_users():
    model = UserModel()
    users = model.getUsers(None, 'json')
    if len(users) == 0:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(users)

@mod_api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    d_filter = {"id": user_id}
    model = UserModel()
    user = model.getUsers(d_filter, 'json')
    if len(user) == 0:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(user)

@mod_api.route('/user', methods=['DELETE'])
def delete_user():
    if not 'id' in request.json :
        return make_response(jsonify({'error': 'Bad parameters'}), 400) 
    errors = validate_json_post(False)
    if(len(errors[0])):
        return make_response(jsonify({'error': 'Bad request', 'errors': errors}), 400)
    d_filter = {"id": int(request.json['id'])}
    model = UserModel()
    user = model.getUsers(d_filter, 'json')
    if len(user) == 0:
        return make_response(jsonify({'error': 'User not found'}), 404)
    model.delete_user(int(request.json['id']))
    return jsonify(user)

@mod_api.route('/user', methods=['PUT'])
def update_user():
    if not request.json :
        return make_response(jsonify({'error': 'Not JSON request'}), 400) 
    if not 'id' in request.json or len(request.json) < 2:
        return make_response(jsonify({'error': 'Bad parameters'}), 400) 
    errors = validate_json_post(False)
    if(len(errors[0])):
        return make_response(jsonify({'error': 'Bad request', 'errors': errors}), 400)
    d_filter = {"id": int(request.json['id'])}
    model = UserModel()
    user = model.getUsers(d_filter)
    if len(user) == 0:
        return make_response(jsonify({'error': 'User not found'}), 404)
    user = user[0]
    if(request.json['username'] != user.username):
        d_filter = {"username": "'"+request.json['username']+"'"}
        model = UserModel()
        user = model.getUsers(d_filter)
        if len(user) != 0:
            errors[0]['username_error'] = "That username is already taken, please choose another"
            return make_response(jsonify({'error': 'Bad request', 'errors': errors}), 400)
    user = User(request.json['id'])
    user.password = crypt.crypt(request.json['password'], getsalt()) if request.json['password'] else None
    user.email = request.json['email'] if request.json['email'] else None
    user.username = re.escape(request.json['username']) if request.json['username'] else None
    user_ret = model.updateUser(user,{'id':request.json['id']}, 'json')
    return jsonify(user_ret), 201


def validate_json_post(requiered):
    js_ret = [{}] 
    if('id' in request.json and (str(request.json['id']).isdigit() != True or int(request.json['id']) < 1)):
        js_ret[0]['username_id_error'] = "Invalid id" 
    if(requiered == True or 'username' in request.json):     
        if(len(request.json['username']) < 4 or len(request.json['username']) > 20):
            js_ret[0]['username_length_error'] = "Usename must be between 4 and 20 characters long"
    if(requiered == True or 'username' in request.json):
        if(re.match("^[a-zA-Z0-9_.-]*$", request.json['username']) == None):
            js_ret[0]['username_match_error'] = "Usename must contain only letters un numbers or underscore"
    if(requiered == True or 'email' in request.json):
        if(len(request.json['email']) < 4 or len(request.json['email']) > 40):
            js_ret[0]['email_length_error'] = "Email must be between 4 and 40 characters long"
    if(requiered == True or 'email' in request.json):
        if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", request.json['email']) == None:
            js_ret[0]['email_match_error'] = "Invalid email address"
    if(requiered == True or 'password' in request.json):
        if(len(request.json['password']) < 4 or len(request.json['password']) > 20):
            js_ret[0]['password_length_error'] = "Password must be between 4 and 20 characters long"
    return js_ret

def getsalt(chars = string.ascii_letters + string.digits):
    return random.choice(chars) + random.choice(chars)