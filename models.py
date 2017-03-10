"""models.py.

Database model classes and JSON serialization functions.
"""

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
        return '<User(email={})>'.format(self.email)


class Category(Base):

    __tablename__ = 'categories'

    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, index=True, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name.strip().title()
        self.slug = Slug(self.name.lower())

    def __repr__(self):
        return '<Category(name={})>'.format(self.name)

    @property
    def serialize(self):
        return dict(id=self.id, title=self.name,
                    items=[i.serialize for i in self.items])


class Item(Base):

    __tablename__ = 'items'

    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, index=True, unique=True, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'Category',
        backref=db.backref('items', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship(
        'User',
        backref=db.backref('items', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, name, category_id, creator_id, description=None):
        self.name = name.strip().title()
        self.slug = Slug(self.name.lower())
        self.category_id = category_id
        self.creator_id = creator_id
        self.description = description

    def __repr__(self):
        return '<Item(name={})>'.format(self.name)

    @property
    def serialize(self):
        return dict(
            id=self.id,
            title=self.name,
            description=self.description,
            categoryID=self.category_id,
            createdDate=self.date_created,
            updatedDate=self.date_updated,
            photos=[p.serialize for p in self.photos]
        )


class ItemPhoto(Base):

    __tablename__ = 'item_photos'

    filename = db.Column(db.String, nullable=False)
    filepath = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship(
        'Item',
        backref=db.backref('photos', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship(
        'User',
        backref=db.backref('item_photos', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, filename, filepath, url, item_id, creator_id):
        self.filename = filename
        self.filepath = filepath
        self.url = url
        self.item_id = item_id
        self.creator_id = creator_id

    def __repr__(self):
        return '<ItemPhoto(filename={})>'.format(self.filename)

    @property
    def serialize(self):
        return dict(id=self.id, filename=self.filename, url=self.url,
                    itemID=self.item_id, createdDate=self.date_created)
