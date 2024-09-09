#!/usr/bin/env python3
""" Country model definition """
from models.base import db, Base


class Country(db.Model):
    """ Country Model """
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name):
        """ Country Initializer """
        self.name = name
