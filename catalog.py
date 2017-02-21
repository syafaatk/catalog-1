from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object('config.DevConfig')

print(app.debug)
print(app.secret_key)
print(app.config['SQLALCHEMY_DATABASE_URI'])


@app.route('/')
def index():
    return render_template('index.html')
