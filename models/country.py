#!/usr/bin/env python3
""" Country model definition """
from models.base import db, Base


class Country(Base):
    """ Country Model """
    __tablename__ = 'countries'

    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name):
        """ Country Initializer """
        self.name = name
