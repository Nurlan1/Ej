# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys
from flask_cors import CORS

os.environ['PORT'] = '5000'

app = Flask('__name__', static_url_path='/static')

app.config['SECRET_KEY'] = 'N'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

import action.view