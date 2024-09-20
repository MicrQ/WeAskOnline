#!/usr/bin/env python3
""" User Model definition """
from models.base import db
from models.country import Country


class User(db.Model):
    """ User model """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
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

    def to_dict(self) -> dict:
        """returns a dict representation of the user data"""
        user = db.session.query(User).filter_by(username=self.username).first()
        return {
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "profile_image": self.profile_image,
            "user_id": user.id
            }
