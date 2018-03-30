from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

os.environ['PORT'] = '5000'
app = Flask ('__name__', static_url_path='/static')

app.config['SECRET_KEY'] = 'N'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////media/nurlan/Lenovo/electronicJournal/Ej/data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import action.view