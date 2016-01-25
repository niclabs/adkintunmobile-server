from flask import render_template
from .. import app


@app.route('/')
def hello_world():
    return render_template('base.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
