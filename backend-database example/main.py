# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from db_manager import DB_Manager
from flask import Flask, render_template, request
from google.cloud import datastore

"""
main class 
will handle with all the requests and will send them to db_manager
"""
app = Flask(__name__)
db_manager = DB_Manager.DB_Manager()


@app.route('/')
def root():
    return '''
              <h1>welcome to kosta's hire challange</h1>
              <p>On this site you can see how to implement a transition between the front-end and the database</p>
              <p> </p>
              <p>we use few methods here:</p>
              get, set, unset, numequalto, undo, redo and end
             <p> please notice that the name need to be unique, Do not use the same name more than once because it will overwrite the data.
              Thanks :) </p>'''


@app.route('/set')
def set_object():
    name = request.args.get('name')
    value = request.args.get('value')

    res = db_manager.set_entity(name, value, True)
    if res:
        return '''
              <h1>The name is : {}</h1>
              <h1>The value is: {}</h1>'''.format(name, value)
    else:
        return '''
        <h1>cant insert the object with the name {} and the value {}</h1>'''.format(name, value)


@app.route('/get')
def get_object():
    name_ = request.args.get('name')
    res = db_manager.get_entity(name_)
    if res:
        return '''
            <h1>The name is : {}</h1>
            <h1>The value is: {}</h1>'''.format(name_, res)
    else:
        return '''
            <h1>cant find the object {}</h1>'''.format(name_)


@app.route('/unset')
def unset_object():
    name_ = request.args.get('name')
    res = db_manager.unset_entity(name_, True)
    ans = db_manager.get_entity(name_)
    if res and ans:
        return '''
            <h1>The name is : {}</h1>
            <h1>The value is: {}</h1>'''.format(name_, res)
    return '''
            <h1>cant update the object with the name {} </h1>'''.format(name_)


@app.route('/numequalto')
def numequalto_value():
    value_ = request.args.get('value')
    ans = db_manager.count_values(str(value_))
    return '''
            <h1>there {} objects with the value: {} </h1>'''.format(ans, value_)


@app.route('/undo')
def do_undo():
    name, value = db_manager.do_undo()
    if name:
        return '''
            <h1>undo: object: {}  with the value: {} </h1>'''.format(name, value)

    return '''<h1>NO COMMANDS</h1>'''


@app.route('/redo')
def do_redo():
    name, value = db_manager.do_redo()
    if name:
        return '''
            <h1>redo: object: {}  with the value: {} </h1>'''.format(name, value)

    return '''<h1>NO COMMANDS</h1>'''


@app.route('/end')
def end():
    db_manager.end()
    return '''<h1>CLEANED</h1>'''


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
