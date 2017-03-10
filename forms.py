"""forms.py.

Pre-built form template classes.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired

from catalog import images


# Catalog item creation and edition form class.
class ItemForm(FlaskForm):
    name = StringField('Item Name', [
        DataRequired('Item name must not be blank.'),
        InputRequired('Item name must not be blank.')
    ])
    description = TextAreaField('Item Description')
    photos = FileField('Photos', [
        FileAllowed(images, 'Images only.')
    ])
    category_id = SelectField('Category', coerce=int)
