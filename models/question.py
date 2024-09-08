#!/usr/bin/env python3
""" Question model definition """
from models.user import User
from models.base import Base, db


class Question(Base):
    """ Question model """
    __tablename__ = 'questions'

    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=True)

    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
