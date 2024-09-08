#!/usr/bin/env python3
""" Base module. Will be used for most models """
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Base(db.Model):
    """ Base model for most models """
    __abstract__ = True
    id = db.Column(db.String(256),
                   primary_key=True,
                   default=lambda: str(uuid4()))
