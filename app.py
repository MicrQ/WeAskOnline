#!/usr/bin/env python3
""" flask app """
from flask import Flask
from api.v1 import comment
from api.v1.auth import auth
from models.base import db
from api.v1.route import home
from api.v1.question import question
from sqlalchemy import text


app = Flask(__name__)
app.url_map.strict_slashes = False
onDevelopment = True
if onDevelopment:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WeAskOnline.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = ''  # production db uri here
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(question)
app.register_blueprint(comment)

with app.app_context():
    if onDevelopment:
        db.session.execute(text('PRAGMA foreign_keys = ON'))
    db.create_all()


@app.errorhandler(404)
def not_found(error):
    """ not found handler """
    return {"Error": "Not found"}, 404


@app.errorhandler(401)
def not_authorized(error):
    """ not authorized handler """
    return {"Error": "Not authorized"}, 401


if __name__ == "__main__":
    app.run(debug=True, port=5000)
