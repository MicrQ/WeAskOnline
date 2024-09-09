#!/usr/bin/env python3
""" user Role model definition """
from models.base import db


class Role(db.Model):
    """ Role model """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name):
        """ Role Initializer """
        self.name = name
