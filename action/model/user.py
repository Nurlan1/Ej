# -*- coding: utf-8 -*-
# from .db import db
from werkzeug.security import generate_password_hash
import uuid
import json
from action import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    teacher = db.Column(db.Boolean)
    student = db.Column(db.Boolean)
    rteacher = db.relationship('Teacher',  backref='user')
    rstudent = db.relationship('Student', backref='user')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, unique=True)
    group_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer)
    phone = db.Column(db.String)
    auth_num = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String)
    attendance = db.relationship('Attendance', backref='student')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    major = db.Column(db.Integer)
    teachers = db.relationship('Teachers_group', backref='group')
    subgroups = db.relationship('SubGroup', backref='group')
    schedule = db.relationship('Schedule', backref='group')


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), unique=True)
    auth_num = db.Column(db.Integer, db.ForeignKey('user.id'))
    groups = db.relationship('Teachers_group', backref='teacher')
    disciplines = db.relationship('Group_discipline', backref='teacher')


class Group_discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    sub_id = db.Column(db.Integer)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    dis_type = db.Column(db.Integer, db.ForeignKey('discipline_type.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class Teachers_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    credit = db.Column(db.Integer)
    academic_hours = db.Column(db.Integer)
    groups = db.relationship('Group_discipline', backref='discipline')
    attendance = db.relationship('Attendance', backref='Discipline')
    schedule = db.relationship('Schedule', backref='Discipline')

class SubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    teacher_id = db.Column(db.Integer)
    sub = db.Column(db.Integer)
    student_id = db.Column(db.Integer)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    dis_type = db.Column(db.Integer, db.ForeignKey('discipline_type.id'))
    status = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default=datetime.utcnow())


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    sub_id = db.Column(db.Integer)
    dis_type = db.Column(db.Integer, db.ForeignKey('discipline_type.id'))
    time = db.Column(db.Integer, db.ForeignKey('class_time.id'))
    week_day = db.Column(db.Integer)
    weeks = db.Column(db.Integer)
    week_type = db.Column(db.Integer)
    auditory = db.Column(db.String(10))


class DisciplineType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    short = db.Column(db.String(10))
    disciplines = db.relationship('Schedule', backref='DisciplineType')


class ExceptionDays(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    todate = db.Column(db.String)


class FirstWeek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)


class ClassTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    begining = db.Column(db.String)
    end = db.Column(db.String)
    disciplines = db.relationship('Schedule', backref='Time')


def adduser(params):
    # db.create_all()
    db.session.add(params)
    db.session.commit()
