"""errors.py.

Custom HTTP error functions.
"""

from flask import render_template, url_for
from flask_wtf.csrf import CSRFError

from catalog import app


@app.errorhandler(CSRFError)
def CSRF_400(err):
    msg = """
        Don't mess with me when I'm sea surfing.
        <br><br>
        (ง'̀-'́)ง"""
    return render_template('error.html', error=err, msg=msg), 400


@app.errorhandler(403)
def forbidden_403(err):
    url = url_for('add_item')
    msg = """
        The item's not yours to modify and destroy.
        <br><br>
        (ノ °益°)ノ 彡
        <br><br>
        <a href="{}">Create</a> to destory.""".format(url)
    return render_template('error.html', error=err, msg=msg), 403


@app.errorhandler(404)
def not_found_404(err):
    url = 'http://marvel.com/avengers'
    msg = """
        On the way to join
        <a href="{}">The Avengers</a>
        and to save the world.
        <br><br>
        ¯\_(ツ)_/¯""".format(url)
    return render_template('error.html', error=err, msg=msg), 404
