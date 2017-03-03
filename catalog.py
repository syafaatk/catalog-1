"""catalog.py.

The main controller module for the entire Catalog project.
"""

import os

from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG', 'config.DevConfig'))

# App wide CSRF protection (Form & AJAX)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
from models import Category, Item, User
db.create_all()

# HTTP error handling functions
import errors

from forms import ItemForm
from decorators import auth_required

# Load the fake data from this module
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
    return redirect(url_for('index'))


def logout():
    session.pop('uid')
    return redirect(url_for('index'))


# Display the category and the items belong to it.
def single_category(category):
    u = User.query.get(session.get('uid', 0))
    c = Category.query.filter_by(slug=category).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    items = Item.query.filter_by(
        category_id=c.id).order_by(Item.date_created.desc()).all()
    return render_template('category.html', user=u, categories=cats,
                           items=items, current_category=c)


# Display the item in details.
def single_item(category, item):
    u = User.query.get(session.get('uid', 0))
    c = Category.query.filter_by(slug=category).first_or_404()
    i = Item.query.filter_by(slug=item, category_id=c.id).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    return render_template('item.html', user=u, categories=cats,
                           current_category=c, item=i)


@auth_required
def add_item():
    u = User.query.get(session.get('uid', 0))
    cats = Category.query.order_by(Category.name).all()
    form = ItemForm()
    form.category_id.choices = [(c.id, c.name) for c in cats]
    if form.validate_on_submit():
        i = Item(form.name.data, form.category_id.data, session['uid'],
                 form.description.data)
        db.session.add(i)
        db.session.commit()
        c = i.category
        return redirect(url_for('item', category=c.slug, item=i.slug))
    return render_template('add_item.html', form=form, user=u,
                           categories=cats)


@auth_required
def edit_item(item):
    u = User.query.get(session.get('uid', 0))
    i = Item.query.filter_by(slug=item).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    form = ItemForm(name=i.name, description=i.description,
                    category_id=i.category_id)
    form.category_id.choices = [(c.id, c.name) for c in cats]
    if form.validate_on_submit():
        form.populate_obj(i)
        db.session.add(i)
        db.session.commit()
        c = i.category
        return redirect(url_for('item', category=c.slug, item=i.slug))
    return render_template('edit_item.html', form=form, user=u, item=i,
                           categories=cats)


@auth_required
def delete_item(item):
    i = Item.query.filter_by(slug=item).first_or_404()
    db.session.delete(i)
    db.session.commit()
    return redirect(url_for('index'))


# URL rules
app.add_url_rule('/', 'index', index)
app.add_url_rule('/catalog/', 'index', index)
app.add_url_rule('/login/', 'login', login)
app.add_url_rule('/logout/', 'logout', logout, methods=['POST'])
app.add_url_rule('/catalog/<category>/', 'category', single_category)
app.add_url_rule('/catalog/<category>/<item>/', 'item', single_item)
app.add_url_rule('/catalog/add/', 'add_item', add_item,
                 methods=['GET', 'POST'])
app.add_url_rule('/catalog/<item>/edit/', 'edit_item', edit_item,
                 methods=['GET', 'POST'])
app.add_url_rule('/catalog/<item>/delete/', 'delete_item', delete_item,
                 methods=['POST'])
