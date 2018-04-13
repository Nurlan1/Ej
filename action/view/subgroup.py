from action.model.user import SubGroup, Group_discipline,Student
from flask import jsonify

def get_sub(id,sub,teacher,subject):
    group= Group_discipline.query.filter_by(group_id=id, sub_id=sub,teacher_id=teacher,discipline_id=subject).first()
    list = SubGroup.query.filter_by(group_id=id, sub=sub, teacher_id=teacher).all()
    print(list)
    output=[]
    for st in list:
        student=Student.query.filter_by(id=st.student_id).first()
        student_data = {}
        student_data['id'] = student.id
        student_data['full_name'] = student.full_name
        student_data['group_id'] = student.group_id
        student_data['status_id'] = student.status_id
        student_data['phone'] = student.phone
        student_data['email'] = student.email
        output.append(student_data)
    return jsonify({'data': output})