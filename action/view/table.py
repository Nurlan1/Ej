# -*- coding: utf-8 -*-
from action import app,db
from flask import jsonify
from action.model.user import User, Group, Group_discipline, Student,DisciplineType, Schedule,FirstWeek,ExceptionDays,ClassTime
from.user import token_required
from .allow_origin import crossdomain
from .subgroup import get_sub
from flask import render_template, request, redirect, url_for, jsonify, make_response

import calendar
import locale
# from flask_cors import cross_origin
import datetime

@app.route('/get_groups', methods=['GET'])
@crossdomain(origin='*')
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

        group  = Group.query.filter_by(id=gr.group_id).first()
        group_data={}
        group_data['id'] = group.id
        group_data['name'] = group.name
        group_data['name_id'] = toLatin(group.name).replace(' ', '')
        group_data['major'] = group.major
        output.append(group_data)
    return jsonify(output)


@app.route('/get_students')
@crossdomain(origin='*')
def get_student():
    students = Student.query.all()
    output = []
    for student in students:


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
@crossdomain(origin='*')
# @cross_origin()
# @token_required
def get_group(id, sub, subject):

    # def get_group(current_user, token, id, sub, subject):
    if sub == '0':
        output = []
        group_list = Student.query.filter_by(group_id=id).all()

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
@crossdomain(origin='*')
# @cross_origin()
# @token_required
def get_discipline(id):
    # current_user, token,
    current_user = User.query.filter_by(id=1).first()
    output = []
    print(id)
    # query = db.session.query(Group_discipline)
    disciplines = Group_discipline.query.filter_by(group_id=id, teacher_id=current_user.rteacher[0].id).group_by(Group_discipline.discipline_id)
    for discipline in disciplines:
        discipline_data = {}
        discipline_data['id'] = discipline.discipline.id
        discipline_data['group_id'] = int(id)
        discipline_data['sub_id'] = discipline.sub_id
        discipline_data['dis_type'] = discipline.dis_type
        discipline_data['dis_tn'] = DisciplineType.query.filter_by(id=discipline.dis_type).first().name
        if discipline.sub_id != 0:
            discipline_data['name'] = discipline.discipline.name + "(" + str(discipline.sub_id) + ")"
        else:
            discipline_data['name'] = discipline.discipline.name
        discipline_data['name_id'] = str(toLatin(discipline.discipline.name) + str(discipline.sub_id)).replace(" ", "")
        discipline_data['credit'] = discipline.discipline.credit
        discipline_data['academic_hours'] = discipline.discipline.academic_hours
        output.append(discipline_data)
    return jsonify({'list_of_discipline': output})

def toLatin(text):
    Rus = ["Я", "я", "Ю", "ю", "Ч", "ч", "Ш", "ш", "Щ", "щ", "Ж", "ж", "А", "а", "Б", "б", "В", "в", "Г", "г", "Д", "д",
           "Е", "е", "Ё", "ё", "З", "з", "И", "и", "Й", "й", "К", "к", "Л", "л", "М", "м", "Н", "н", "О",
           "о", "П", "п",
           "Р", "р", "С", "с", "Т", "т", "У", "у", "Ф", "ф", "Х", "х", "Ц", "ц", "Ы", "ы", "Ь", "ь", "Ъ", "ъ", "Э", "э"]

    Eng = ["Ya", "ya", "Yu", "yu", "Ch", "ch", "Sh", "sh", "Sh", "sh", "Zh", "zh", "A", "a", "B", "b", "V", "v", "G",
           "g", "D", "d", "E", "e", "E", "e", "Z", "z", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N",
           "n", "O",
           "o", "P", "p", "R", "r", "S", "s", "T", "t", "U", "u", "F", "f", "H", "h", "C", "c", "Y", "y", "", "", "\"",
           "\"", "E", "e"]
    translation = ''''''
    for i in range(len(text)):
        try:
            j = Rus.index(text[i])
            translation += Eng[j]
        except:
            translation+=text[i]
    return str(translation)


@app.route('/get_type/<id>&dis=<dis>&sub=<sub>', methods=['GET'])
@crossdomain(origin='*')
def get_type(id,dis,sub):
    # current_user, token,
    current_user = User.query.filter_by(id=1).first()
    types = Group_discipline.query.filter_by(group_id=id, teacher_id=current_user.rteacher[0].id, discipline_id=dis, sub_id=sub).all()
    output=[]
    for type in types:
        type_data={}
        type_data['dis_type'] = type.dis_type
        type_data['dis_tn'] = DisciplineType.query.filter_by(id=type.dis_type).first().name
        type_data['tn_eng']= toLatin(str(DisciplineType.query.filter_by(id=type.dis_type).first().name))
        output.append(type_data)
    return jsonify({'type_of_discipline': output})


@app.route('/get_date/id=<id>&dis=<dis>&sub=<sub>&type=<dtype>', methods=['GET'])
@crossdomain(origin='http://localhost:8000')
def get_date(id, dis, sub, dtype):
    current_user = User.query.filter_by(id=1).first()
    infos = Schedule.query.filter_by(group_id=id, teacher_id=current_user.rteacher[0].id, discipline_id=dis, sub_id=sub, dis_type=dtype).all()
    exceptions = ExceptionDays.query.all()
    print(infos)
    dates=[]
    for info in infos:
        today = datetime.datetime.strptime(FirstWeek.query.filter_by(id=1).first().date, "%Y-%m-%d")
        daydif = (info.week_day-1)-today.weekday()
        interval = 2
        if info.week_type == 0:
            interval = 1
        elif info.week_type == 1:
            interval = 2
        else:
            today = today-datetime.timedelta(weeks=1)
        today = today + datetime.timedelta(days=daydif, weeks=-interval)
        for i in range(int(int(info.weeks)/len(infos))):
            next_monday = today + datetime.timedelta(weeks=interval)
            today=next_monday
            for exception in exceptions:
                if exception.date == str(next_monday.date()):
                    dates.append(exception.todate)
                else:
                    dates.append(str(next_monday.date()))
    dates = sorted(dates)
    # print(dates)
    months = ['Январь' , 'Февраль' , 'Март' , 'Апрель' , 'Май' , 'Июнь' , 'Июль' , 'Август' , 'Сентябрь' , 'Октябрь' , 'Ноябрь' , 'Декабрь'];
    # print(months[int(dates[0][5:-3])-1])
    output=[]
    m = []
    for i in range(len(dates)-1):
        dat = {}
        month = int(dates[i][5:-3])-1
        m.append(int(dates[i][8:]))

        if month !=int(dates[i+1][5:-3])-1:
            dat['month'] = months[month]
            dat['dates'] = m
            output.append(dat)
            m = []
            print(output)


    return jsonify(output)


@app.route('/schedule', methods=["GET"])
@crossdomain(origin='*')
def schedule():
    date = request.args.get('date')
    date = datetime.date(int(date[:4]), int(date[5:7]), int(date[-2:])).weekday()
    schedule = Schedule.query.filter_by(teacher_id=1, week_day=date).all()
    lessons=[]
    for clas in schedule:
        lesson = {}
        group={}
        lesson["type"] = clas.DisciplineType.name
        lesson["id"] = clas.discipline_id
        lesson["name"] = clas.Discipline.name
        lesson["group"] = {"id": clas.group_id,
                         "name": clas.group.name}
        lesson["desciption"]="Плана нет пока!"
        lesson["sub_group"]=clas.sub_id
        lesson["beginning"] =clas.Time.begining
        lesson["end"] = clas.Time.end
        lesson["auditory"] = clas.auditory
        lessons.append(lesson)

    rooms = set(d.get('auditory') for d in lessons)
    classrooms=[]
    for room in rooms:
        new_dict={}
        new_dict["name"]=room
        disciplines=[]
        for lesson in lessons:
            if room == lesson.get('auditory'):
                disciplines.append(lesson)
                lesson.pop('auditory', None)
        new_dict["lessons"]=disciplines
        classrooms.append(new_dict)


    # create a dictionary
    # new_dict = {}
    #
    # # iterate over the unique film names
    # for k in lessons:
    #     # make a list of all the films that match the name we're on
    #     filmswiththisname = [d for d in lessons if d.get('auditory') == k]
    #     # add the list of films to the new dictionary with the film name as the key.
    #     new_dict[k] = filmswiththisname

    return jsonify({'classRooms': classrooms})


@app.route('/loggin', methods=['POST'])
def loggin():
    login=request.values['username']
    password=request.values['password']
    print(login,password)
    return '0'
