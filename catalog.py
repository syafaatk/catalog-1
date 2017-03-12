"""catalog.py.

The main controller module for the entire Catalog project.
"""

import json
import os

from datetime import date
from uuid import uuid4

import bleach
import httplib2

from apiclient import discovery
from oauth2client import client
from flask import (Flask, render_template, session, redirect, make_response,
                   url_for, request, send_from_directory, jsonify, Markup,
                   g, flash)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_uploads import (UploadSet, IMAGES, configure_uploads,
                           patch_request_class)

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG', 'config.DevConfig'))

# App wide CSRF protection (Form & AJAX)
csrf = CSRFProtect(app)

# Flask-Uploads configurations for image uploading
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app, 5 * 1024 * 1024)  # 5 MB at most

db = SQLAlchemy(app)
from models import Category, Item, ItemPhoto, User
db.create_all()

# HTTP error handling functions
import errors

from forms import ItemForm
from decorators import auth_required

# TODO: Remove on final production version
# Load the fake data from this module
import load_db


# Jinja 2 Template functions
@app.context_processor
def utility_processor():
    def bleach_clean(s):
        return Markup(bleach.clean(s).replace('\n', '<br>'))
    return dict(bleach_clean=bleach_clean)


# Set all the app wide data
@app.before_request
def get_general_data():
    g.APP_NAME = 'Catalog'
    g.COPYRIGHT_YEAR = date.today().strftime('%Y')
    g.G_CLIENT_ID = '717661788461-hvt4hniaeqpeg7gt9dsmtgpvhbv8hsku.apps.googleusercontent.com'


def resp(http_code=200, message=None, content_type='application/json'):
    """Return an HTTP response object.

    Keyword arguments:
    http_code -- the HTTP status code. Defaults to 200.
    message -- the message to be responded to user. Defaults to None.
    content_type -- the content type header. Defaults to 'application/json'.
    """
    resp_ = make_response(json.dumps(message), http_code)
    resp_.headers['Content-Type'] = content_type
    return resp_


# Google OAuth sign in
def g_login():
    if session.get('uid'):
        return resp(message='Already logged in.')

    if not request.headers.get('X-Requested-With'):
        return resp(403, 'Potential CSRF attack.')
    auth_code = request.data
    CLIENT_SECRET_FILE = 'client_secret.json'

    # Exchange auth code for access token, refresh token and ID token
    try:
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['openid', 'profile', 'email'],
            auth_code
        )
    except client.FlowExchangeError:
        return resp(401, 'Code exchange failed.')

    # Call Google API
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('plus', 'v1', http=http_auth)
    profile = service.people().get(userId='me').execute()

    # Get profile info from ID token
    google_uid = credentials.id_token['sub']
    email = credentials.id_token['email']
    name = profile['displayName']
    photo = profile['image']['url']

    # Create user or not
    u = User.query.filter_by(google_uid=google_uid).first()
    if not u:
        u = User(name, email, photo, google_uid)
        db.session.add(u)
        db.session.commit()
    session.update(uid=u.id, google_uid=google_uid, provider='google',
                   credentials=credentials.to_json())
    return resp(message='Everything looks good.')


# Revoke Google OAuth access
def revoke_g_access():
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    revocation = credentials.revoke(httplib2.Http())
    if revocation is not None:
        return resp(400, 'Token revocation failed.')
    return resp('Revocation done.')


def index():
    u = User.query.get(session.get('uid', 0))  # User may or may not exist
    cats = Category.query.order_by(Category.name).all()
    items = Item.query.order_by(Item.date_created.desc()).all()
    return render_template('index.html', user=u, categories=cats, items=items)


def logout():
    if 'uid' not in session:
        flash('You must log in to log out, huh!', 'warning')
        return redirect(url_for('index', _anchor='login'))
    if session.get('provider') == 'google':
        # revoke_g_access()
        pass
    session.clear()
    if request.is_xhr:
        return resp(message='Logged out.')
    return redirect(url_for('index'))


# Display the category and the items belong to it.
def single_category(category):
    u = User.query.get(session.get('uid', 0))  # User may or may not exist
    c = Category.query.filter_by(slug=category).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    items = Item.query.filter_by(
        category_id=c.id).order_by(Item.date_created.desc()).all()
    return render_template('category.html', user=u, categories=cats,
                           items=items, current_category=c)


# Display the item in details.
def single_item(category, item):
    u = User.query.get(session.get('uid', 0))  # User may or may not exist
    c = Category.query.filter_by(slug=category).first_or_404()
    i = Item.query.filter_by(slug=item, category_id=c.id).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    return render_template('item.html', user=u, categories=cats,
                           current_category=c, item=i)


# Get uploaded photos from the server
def uploaded_file(year, month, day, filename):
    dest = '{}/{}/{}/{}/'.format(app.config['UPLOADED_IMAGES_DEST'],
                                 year, month, day)
    return send_from_directory(dest, filename)


# Upload the file to the server file system
def upload_file(file):
    sub_folder = date.today().strftime('%Y/%m/%d')
    new_filename = str(uuid4()).replace('-', '')[::-1] + '.'
    return images.save(file, sub_folder, new_filename)


# Return the collections of ItemPhoto objects
def get_item_photo_list(item_id):
    photos = []
    for photo in request.files.getlist('photos'):
        if not photo.filename:
            break
        filename = upload_file(photo)
        photos.append(
            ItemPhoto(filename.rsplit('/')[-1], images.path(filename),
                      images.url(filename), item_id, session['uid'])
        )
    return photos


@auth_required
def add_item():
    u = User.query.get(session.get('uid', 0))  # User must exist
    cats = Category.query.order_by(Category.name).all()
    form = ItemForm()
    form.category_id.choices = [(c.id, c.name) for c in cats]
    if form.validate_on_submit():
        i = Item(form.name.data, form.category_id.data, session['uid'],
                 form.description.data)
        if 'photos' in request.files:
            i.photos = get_item_photo_list(i.id)
        db.session.add(i)
        db.session.commit()
        c = i.category
        return redirect(url_for('item', category=c.slug, item=i.slug))
    return render_template('add_item.html', form=form, user=u,
                           categories=cats)


@auth_required
def edit_item(item):
    u = User.query.get(session.get('uid', 0))  # User must exist
    i = Item.query.filter_by(slug=item).first_or_404()
    cats = Category.query.order_by(Category.name).all()
    form = ItemForm(name=i.name, description=i.description,
                    category_id=i.category_id)
    form.category_id.choices = [(c.id, c.name) for c in cats]
    if form.validate_on_submit():
        if 'photos' in request.files:
            photos = get_item_photo_list(i.id)
            db.session.add_all(photos)
            db.session.commit()
            form.photos.data = ItemPhoto.query.filter_by(item_id=i.id).all()
        form.populate_obj(i)
        db.session.add(i)
        db.session.commit()
        c = i.category
        return redirect(url_for('item', category=c.slug, item=i.slug))
    return render_template('edit_item.html', form=form, user=u, item=i,
                           categories=cats)


# Delete uploaded file from both database and file system
def delete_file(filepath):
    try:
        os.remove(filepath)
    except OSError:
        pass  # Ignore FileNotFoundError


@auth_required
def delete_photo(photo_id):
    p = ItemPhoto.query.filter_by(id=photo_id).first_or_404()
    delete_file(p.filepath)
    db.session.delete(p)
    db.session.commit()
    return resp(message='Photo deleted.')


# TODO: Implement Client side Forbidden error.
@auth_required
def delete_item(item):
    i = Item.query.filter_by(slug=item).first_or_404()
    for p in i.photos:
        delete_file(p.filepath)
    db.session.delete(i)
    db.session.commit()
    if request.is_xhr:
        return resp(message='Item deleted.')
    return redirect(url_for('index'))


# JSON endpoints
def JSON_catalog():
    categories = Category.query.order_by(Category.name).all()
    return jsonify(Categories=[c.serialize for c in categories])


def JSON_single_category(id):
    c = Category.query.get_or_404(id)
    return jsonify(Category=c.serialize)


def JSON_single_item(id):
    i = Item.query.get_or_404(id)
    return jsonify(Item=i.serialize)


# Browser JS is disabled.
def nojs():
    title = 'JavaScript is disabled'
    return render_template('nojs.html', title=title)


# URL rules
app.add_url_rule('/', 'index', index)
app.add_url_rule('/login/google/', 'g_login', g_login, methods=['POST'])
app.add_url_rule('/logout/', 'logout', logout, methods=['POST'])
app.add_url_rule('/catalog/', 'index', index)
app.add_url_rule('/catalog/<category>/', 'category', single_category)
app.add_url_rule('/catalog/<category>/<item>/', 'item', single_item)
app.add_url_rule('/catalog/add/', 'add_item', add_item,
                 methods=['GET', 'POST'])
app.add_url_rule('/catalog/<item>/edit/', 'edit_item', edit_item,
                 methods=['GET', 'POST'])
app.add_url_rule('/catalog/<item>/delete/', 'delete_item', delete_item,
                 methods=['POST'])
app.add_url_rule('/usercontent/img/<year>/<month>/<day>/<filename>/',
                 'uploaded_file', uploaded_file)
app.add_url_rule('/usercontent/img/<int:photo_id>/delete/', 'delete_photo',
                 delete_photo, methods=['POST'])
app.add_url_rule('/json/', 'JSON_catalog', JSON_catalog)
app.add_url_rule('/json/catalog/', 'JSON_catalog', JSON_catalog)
app.add_url_rule('/json/category/<int:id>/', 'JSON_category',
                 JSON_single_category)
app.add_url_rule('/json/item/<int:id>/', 'JSON_item',
                 JSON_single_item)
app.add_url_rule('/nojs/', 'nojs', nojs)
