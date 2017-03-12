from random import randint

from catalog import db
from models import User, Category, Item


# if not User.query.count():
#     print('Loading User data ...')
#     users = [
#         User('Andrea Bocelli', 'abocelli@gmail.com'),
#         User('Louise', 'lou@gmail.com'),
#         User('Simon Pegg', 'spegg@yahoo.com'),
#         User('Daisy Ridley', 'dridley@yahoo.com'),
#         User('Ben Affleck', 'baffleck@yahoo.com'),
#         User('Bryce Dallas Howard', 'bdhoward@yahoo.com'),
#         User('Matt Damon', 'mdamon@yahoo.com'),
#         User('Zoe Saldana', 'zsaldana@yahoo.com'),
#     ]
#     db.session.add_all(users)
#     db.session.commit()


if not Category.query.count():
    print('Loading Category data ...')
    cats = [
        Category('Snowboarding'),   # ID 1
        Category('Skating'),        # ID 2
        Category('Soccer'),         # ID 3
        Category('Basketball'),     # ID 4
        Category('Baseball'),       # ID 5
        Category('Frisbee'),        # ID 6
        Category('Rock Climbing'),  # ID 7
        Category('Foosball'),       # ID 8
        Category('Hockey'),         # ID 9
    ]
    db.session.add_all(cats)
    db.session.commit()


# if not Item.query.count():
#     print('Loading Item data ...')
#     ul = len(users)
#     items = [
#         Item('Skate Board', 2, randint(1, ul), 'Skate board for human.'),
#         Item('Goggles', 1, randint(1, ul), 'Goggles for snowboarding.'),
#         Item('Bat', 5, randint(1, ul), 'The bat used by the Dark Knight.'),
#         Item('Stick', 9, randint(1, ul), 'Stick made of gold for Hockey'),
#     ]
#     db.session.add_all(items)
#     db.session.commit()
