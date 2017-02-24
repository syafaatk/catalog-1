import os

from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG', 'config.DevConfig'))

db = SQLAlchemy(app)
from models import Category, Item, User
db.create_all()
import load_db

print(app.debug)
print(app.secret_key)
print(app.config['SQLALCHEMY_DATABASE_URI'])


def index():
    u = User.query.get(session.get('uid', 0))
    cats = Category.query.order_by(Category.name)
    items = Item.query.order_by(Item.name)
    return render_template('index.html', user=u, categories=cats, items=items)


def login():
    # Fake user sign in
    if 'uid' not in session:
        from random import randint
        session['uid'] = randint(1, 8)
    return redirect(url_for('index'))


def logout():
    session.pop('uid')
    return redirect(url_for('index'))


# URL rules
app.add_url_rule('/', 'index', index)
app.add_url_rule('/catalog/', 'index', index)
app.add_url_rule('/login/', 'login', login)
app.add_url_rule('/logout/', 'logout', logout, methods=['POST'])
