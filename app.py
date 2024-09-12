#!/usr/bin/env python3
""" flask app """
from flask import Flask
from api.v1.auth import auth
from models.base import db
from api.v1.route import home
from sqlalchemy import text


app = Flask(__name__)
onDevelopment = True
if onDevelopment:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WeAskOnline.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = '' # production db uri here
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(home)

with app.app_context():
    if onDevelopment:
        db.session.execute(text('PRAGMA foreign_keys = ON'))
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
