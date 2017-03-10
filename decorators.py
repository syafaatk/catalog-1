"""decorators.py.

Decorator functions and classes for authentication and authorization.
"""

from functools import wraps

from flask import session, request, redirect, url_for, abort

from models import Item, ItemPhoto


def auth_required(f):
    """A decorator to force the user to do auth related things.

    Force the user to authenticate her identity.
    If already logged in, check user's authorization
    to edit and delete items and photos.
    """
    @wraps(f)
    def f_wrapper(*args, **kwargs):
        if 'uid' not in session:
            return redirect(url_for('index', next=request.url,
                                    _anchor='login'))
        item_slug = kwargs.get('item')
        if item_slug:
            i = Item.query.filter_by(slug=item_slug).first_or_404()
            if i.creator_id != session.get('uid'):
                abort(403)
        photo_id = kwargs.get('photo_id')
        if photo_id:
            p = ItemPhoto.query.filter_by(id=photo_id).first_or_404()
            if p.creator_id != session.get('uid'):
                abort(403)
        return f(*args, **kwargs)
    return f_wrapper
