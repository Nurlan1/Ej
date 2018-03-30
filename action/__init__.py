from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask ('__name__')

app.config['SECRET_KEY'] = 'N'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////media/nurlan/Lenovo/electronicJournal/Ej/data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import action.view