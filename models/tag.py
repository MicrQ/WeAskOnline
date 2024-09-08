#!/usr/bin/env python3
""" Tag model implementation """
from models.base import Base, db


class Tag(Base):
    """ Tag model """
    __tablename__ = 'tags'

    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name):
        """ Tag Initializer """
        self.name = name
