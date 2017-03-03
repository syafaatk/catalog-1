"""forms.py.

Pre-built form template classes.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired


# Catalog item creation and edition form class.
class ItemForm(FlaskForm):
    name = StringField('Item Name', [
        DataRequired('Item name must not be space.'),
        InputRequired('Item name must not be blank.')
    ])
    description = TextAreaField('Item Description')
    category_id = SelectField('Category', coerce=int)
