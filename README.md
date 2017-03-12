# Catalog
A catalog app where user can add items to certain categories.

## Setup
First, create a [python3 virtualenv environment](https://virtualenv.pypa.io/en/stable/).

Then, do the following commands in the terminal.
```
$ git clone https://github.com/gitzart/catalog.git
$ cd catalog/
$ pip install -r requirements.txt
```

## Usage
The app can be run like this
```
$ gunicorn -b :5000 wsgi:app
```
or this
```
$ python wsgi.py
```
Now the app is listening on port `5000` of `localhost`, [http://localhost:5000](http://localhost:5000).

## Or
Visit [https://flasca.herokuapp.com](https://flasca.herokuapp.com)
