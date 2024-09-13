#!/usr/bin/env python3
""" Question model definition """
from email.policy import default
from models.user import User
from models.base import db
from datetime import datetime, timezone


class Question(db.Model):
    """ Question model """
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.now(timezone.utc),
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now(timezone.utc),
                           nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=True)

    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    user = db.relationship('User',
                           backref=db.backref('questions', lazy=True))

    def __init__(self, title, body,
                 user_id, updated_at=None):
        """ Question Initializer """
        self.title = title.title()
        self.body = body.title()
        self.user_id = user_id
        if updated_at:
            self.updated_at = updated_at
