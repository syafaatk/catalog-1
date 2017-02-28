import os

from flask import Flask, render_template, session, redirect, url_for, flash
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
    cats = Category.query.order_by(Category.name).all()
    items = Item.query.order_by(Item.date_created.desc()).all()
    return render_template('index.html', user=u, categories=cats, items=items)


def login():
    # Fake user sign in
    if 'uid' not in session:
        from random import randint
        session['uid'] = randint(1, 8)
    flash('You have been logged in.', 'info')
    return redirect(url_for('index'))


def logout():
    session.pop('uid')
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


def single_category(category):
    u = User.query.get(session.get('uid', 0))
    c = Category.query.filter_by(slug=category).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    items = Item.query.filter_by(
        category_id=c.id).order_by(Item.date_created.desc()).all()
    return render_template('category.html', user=u, categories=cats,
                           items=items, current_category=c)


def single_item(category, item):
    u = User.query.get(session.get('uid', 0))
    c = Category.query.filter_by(slug=category).first_or_404()
    i = Item.query.filter_by(slug=item, category_id=c.id).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    return render_template('item.html', user=u, categories=cats,
                           current_category=c, item=i)


# URL rules
app.add_url_rule('/', 'index', index)
app.add_url_rule('/catalog/', 'index', index)
app.add_url_rule('/login/', 'login', login)
app.add_url_rule('/logout/', 'logout', logout, methods=['POST'])
app.add_url_rule('/catalog/<category>/', 'category', single_category)
app.add_url_rule('/catalog/<category>/<item>/', 'item', single_item)
