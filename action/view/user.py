# -*- coding: utf-8 -*-
from action import app
from action.controller import addusercontroller
from action.model.user import User, Group, Group_discipline,Teachers_group
from werkzeug.security import generate_password_hash
import uuid
from flask import render_template, request, redirect, url_for, jsonify, make_response
from werkzeug.security import check_password_hash
import jwt
import datetime
from action import db
from functools import wraps
@app.route('/newuser', methods=['GET','POST'])
def adduser():
    # db.create_all()
    if request.method == 'POST':
        data = request.form
        print(data['password'])
        hashed_password = generate_password_hash(data['password'], method='sha256')
        admin = 0
        student = 0
        teacher = 0
        try:
            if data['admin']=='on':
                admin = 1
        except:
            admin = 0
        try:
            if data['student']=='on':
                student = 1
        except:
            student = 0
        try:
            if data['teacher']=='on':
                teacher = 1
        except:
            teacher = 0
        try:
            new_user = User(public_id=str(uuid.uuid4()), name=data['username'], password=hashed_password, admin=admin, teacher=teacher, student=student)
            print(new_user)
            addusercontroller(new_user)
        except:
            return 'Already exists'
    else:
        return render_template('register.html')
    return 'User is added'

def token_required(f):
     @wraps(f)
     def decorated(*args, **kwargs):

         token= None
         refresh_token=None
         if 'Cookie' in request.headers:
             token = request.cookies.get('x-access-token')
             refresh_token = request.cookies.get('x-refresh-token')
         if not token and not refresh_token:
                return 'token is missing',401
         try:
             data = jwt.decode(token, app.config['SECRET_KEY'])
             current_user = User.query.filter_by(public_id=data['public_id']).first()


         except:
            try:
             data = jwt.decode(refresh_token, app.config['SECRET_KEY'])
             current_user = User.query.filter_by(public_id=data['public_id']).first()
             token = jwt.encode({'public_id': current_user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
            except:
                return 'token is invalid', 401

         return f(current_user, token, *args, **kwargs)
     return decorated


@app.route('/', methods=['GET', 'POST'])
def login():
    form = request.form
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        print(name)
        user_info = User.query.filter_by(name=name).first()
        if user_info == None:
            return render_template('login.html', form=form, info="Неправильный логин или пароль...")
        elif check_password_hash(user_info.password, password):
            token = jwt.encode({'public_id': user_info.public_id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=35)}, app.config['SECRET_KEY'])
            refresh_token = jwt.encode({'public_id': user_info.public_id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=500)}, app.config['SECRET_KEY'])
            resp = make_response(redirect(url_for('logged', public_Id=user_info.public_id)))
            resp.set_cookie('x-access-token', token)
            resp.set_cookie('x-refresh-token', refresh_token)
            return resp
        else:
            return render_template('login.html', form=form, info="Неправильный логин или пароль...", user="nurik")
    return render_template('login.html', form=form)


@app.route('/logged/<public_Id>', methods=['GET'])
@token_required
def logged(current_user, token, public_Id):

    resp = make_response(render_template('index.html', name=current_user.name))
    resp.set_cookie('x-access-token', token)
    return resp


@app.route('/logout', methods=['GET'])
@token_required
def logout(current_user, token):

    resp=make_response(redirect('/'))
    resp.set_cookie('x-access-token', expires=0)
    resp.set_cookie('x-refresh-token', expires=0)
    return resp