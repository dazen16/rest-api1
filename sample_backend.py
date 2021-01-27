from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import random

from mongodb import User

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = { 
   'users_list' :
   ["""
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }"""
   ]    
}

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username and search_job:
         # return find_users_by_name_job(search_username, search_job)
         return User().find_by_name_job(search_username, search_job)
      elif search_username:
         users = User().find_by_name(search_username)
      elif search_job:
         #return find_users_by_job(search_job)
         users = User().find_by_job(search_job)
      else:
         users = User().find_all()
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      # userToAdd['id'] = random.randint(100000, 999999) #adding unique id's
      # users['users_list'].append(userToAdd)

      newUser = User(userToAdd)
      newUser.save()

      resp = jsonify(newUser), 201 #returning json object
      # resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp
   elif request.method == 'DELETE':
      userToDel = request.get_json()
      # users['users_list'].remove(userToDel)
      delUser = User(userToDel)
      delUser.remove()

      resp = jsonify(success = True), 200
      return resp

@app.route('/users/<id>')
def get_user(id):
   if id :
      for user in users['users_list']:
        if user['id'] == id:
           return user
      return ({})
   return users

def find_users_by_name_job(name, job):
  subdict = {'users_list' : []}
  for user in users['users_list']:
    if user['name'] == name and user['job'] == job:
      subdict['users_list'].append(user)
  return subdict

def find_users_by_job(job):
  subdict = {'users_list' : []}
  for user in users['users_list']:
    if user['job'] == job:
      subdict['users_list'].append(user)
  return subdict

