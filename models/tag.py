#!/usr/bin/env python3
""" Tag model implementation """
from models.base import db


class Tag(db.Model):
    """ Tag model """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name):
        """ Tag Initializer """
        self.name = name.lower()
    
    def to_dict(self):
        """ returns the dictionary version of the model """
        return {
            'id': self.id,
            'name': self.name
        }
