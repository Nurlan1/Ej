# -*- coding: utf-8 -*-
from action import app
from flask import jsonify
from action.model.user import User, Group, Group_discipline, Student
from.user import token_required
from .allow_origin import crossdomain
from .subgroup import get_sub

@app.route('/get_groups', methods=['GET'])
# @token_required
def get_groups():
    current_user = User.query.filter_by(id=1).first()
    groups=current_user.rteacher[0].groups
    # teacher1 = Discipline.query.filter_by(id=1).all()
    #
    # print(teacher1)
    # groups = Teachers_group.query.filter_by(teacher_id=current_user.id).all()
    # # print(groups)
    output = []
    for gr in groups:
        print(gr)
        group  = Group.query.filter_by(id=gr.group_id).first()
        group_data={}
        group_data['id'] = group.id
        group_data['name'] = group.name
        group_data['major'] = group.major
        output.append(group_data)
    return jsonify({'groups': output})

@app.route('/get_students')
def get_student():
    students = Student.query.all()
    output = []
    for student in students:
        print(student)
        student_data = {}
        student_data['id']=student.id
        student_data['full_name']= student.full_name
        student_data['group_id'] = student.group_id
        student_data['status_id'] = student.status_id
        student_data['phone'] = student.phone
        student_data['email'] = student.email
        output.append(student_data)
    return jsonify({'groups': output})
@app.route('/get_group/id=<id>&sub=<sub>&dis=<subject>', methods=['GET'])
@crossdomain(origin='http://localhost:8000')
# @token_required
def get_group(id,sub,subject):

    # def get_group(current_user, token, id, sub, subject):
    if sub == '0':
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
        return jsonify(output)
    else:
        return get_sub(id, sub, 1, subject)



@app.route('/get_disciplines/<id>', methods=['GET'])
# @token_required
def get_discipline(id):
    # current_user, token,
    current_user = User.query.filter_by(id=1).first()
    output = []
    disciplines = Group_discipline.query.filter_by(group_id=id, teacher_id=current_user.rteacher[0].id).all()
    for discipline in disciplines:
        discipline_data = {}
        discipline_data['id'] = discipline.discipline.id
        discipline_data['sub_id'] = discipline.sub_id
        if discipline.sub_id!=0:
            discipline_data['name'] = discipline.discipline.name + "(" + str(discipline.sub_id) + "подгруппа)"
        else:

            discipline_data['name'] = discipline.discipline.name
        discipline_data['credit'] = discipline.discipline.credit
        discipline_data['academic_hours'] = discipline.discipline.academic_hours
        output.append(discipline_data)
    return jsonify({'list_of_discipline': output})
