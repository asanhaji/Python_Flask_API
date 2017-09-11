from Flask_D01 import db
import crypt
import random, string
import re
from flask import url_for


class User(object):
    def __init__(self, _id = None, username = None, email = None, password = None):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
    def set_username(self, username):
        self.username = username
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password

class UserModel(object):
    def __init__(self):
        pass

    def getsalt(self,chars = string.ascii_letters + string.digits):
        return random.choice(chars) + random.choice(chars)

    def getUsers(self, d_filter=None,type="array"):
        query_dict = {'table': 'users', 'columns': []}
        db_ret = db.select(query_dict, d_filter)
        if(type == "json"):
            ret = self.serialize_to_json(db_ret)
        else:
            ret = self.serialize_to_users(db_ret)
        return ret
    
    def updateUser(self,user,d_filter,type="array"):
        query_dict = {'table': 'users'}
        if(user.password):
            query_dict['password'] = "'"+user.password+"'"
        if(user.username):
            query_dict['username'] = "'"+user.username+"'"
        if(user.email):
            query_dict['email'] = "'"+user.email+"'"
        db_ret = db.update(query_dict, d_filter)
        if(type == "json"):
            ret = self.serialize_to_json(db_ret)
        else:
            ret = self.serialize_to_users(db_ret)
        return ret 

    def addUser(self, user, type="array"):
        query_dict = {'table': 'users', 'username': user.username, 'password': user.password, 'email': user.email}
        db_ret = db.insert(query_dict)
        if(type == "json"):
            ret = self.serialize_to_json(db_ret)
        else:
            ret = self.serialize_to_users(db_ret)
        return ret

    def delete_user(self, _id, type="array"):
        db_ret = db.delete('users', {'id': _id})
        print(db_ret)

    def serialize_to_json(self, obj):
        ret = [dict(u) for u in obj]
        new_field = {}
        for i in range(len(ret)):
            del ret[i]['password']
            ret[i]['uri'] = ""
            for key, value in ret[i].items():
                if(key == 'id'):
                    ret[i]['uri'] = url_for('api.get_user', user_id=value, _external = True)    
            del ret[i]['id']
        return ret

    def serialize_to_users(self, obj):
        nobj = [dict(u) for u in obj]
        arr = []
        for i in range(len(nobj)):
            u = User(nobj[i]['id'], nobj[i]['username'], nobj[i]['email'], nobj[i]['password'])
            arr.append(u)
        return arr

        
                

