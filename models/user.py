#!/usr/bin/env python3
""" User Model definition """
from models.base import Base, db
from models.country import Country


class User(Base):
    """ User model """
    __tablename__ = 'users'

    firstname = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(256))
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    country_id = db.Column(db.Integer,
                           db.ForeignKey('countries.id', ondelete='CASCADE'),
                           nullable=False)
    profile_image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=True)

    country = db.relationship('Country',
                              backref=db.backref('users', lazy=True))

    def __init__(self, firstname, lastname,
                 bio, username, email, password,
                 created_at, updated_at, country_id,
                 profile_image=None, isActive=True):
        """ User Initializer """
        self.firstname = firstname
        self.lastname = lastname
        self.bio = bio
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.country_id = country_id
        self.profile_image = profile_image
        self.isActive = isActive
