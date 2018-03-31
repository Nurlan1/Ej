# -*- coding: utf-8 -*-
from action import app
from flask import jsonify
from action.model.user import Group, Student

from.user import token_required

@app.route('/get_groups', methods=['GET'])
# @token_required
def get_groups():

    groups=Group.query.all()
    print(groups)
    output=[]
    for group in groups:
        group_data={}
        group_data['id'] = group.id
        group_data['name'] = group.name
        group_data['major'] = group.major
        output.append(group_data)
    return jsonify({'groups' : output})
@app.route('/get_group/<id>', methods=['GET'])
# @token_required
def get_group(id):
    output = []
    group_list = Student.query.filter_by(group_id=id).all()
    print(group_list)
    for student in group_list:
        student_data = {}
        student_data['id'] = student.id
        student_data['full_name'] = student.full_name
        student_data['group_id'] = student.group_id
        student_data['status_id'] = student.status_id
        student_data['phone'] = student.phone
        student_data['email'] = student.email
        output.append(student_data)
    return jsonify({'list_of_group': output})
