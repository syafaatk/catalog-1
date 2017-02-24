from datetime import datetime

from slugify import UniqueSlugify

from catalog import db


Slug = UniqueSlugify(translate=None)


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, onupdate=datetime.now)


class User(Base):

    __tablename__ = 'users'

    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, index=True, unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User(email={0})>'.format(self.email)


class Category(Base):

    __tablename__ = 'categories'

    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, index=True, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name.strip().title()
        self.slug = Slug(self.name.lower())

    def __repr__(self):
        return '<Category(name={0})>'.format(self.name)


class Item(Base):

    __tablename__ = 'items'

    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, index=True, unique=True, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'Category',
        backref=db.backref('items', lazy='dynamic')
    )
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship(
        'User',
        backref=db.backref('items', lazy='dynamic')
    )

    def __init__(self, name, category_id, creator_id, description=None):
        self.name = name.strip().title()
        self.slug = Slug(self.name.lower())
        self.category_id = category_id
        self.creator_id = creator_id
        self.description = description

    def __repr__(self):
        return '<Item(name={0})>'.format(self.name)