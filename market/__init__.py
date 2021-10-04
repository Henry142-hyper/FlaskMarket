from flask import Flask, render_template, flash, get_flashed_messages, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd754e1c3e16ca4d7cd62252c9bfc7ef2b9dca2df939935d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from market import routes