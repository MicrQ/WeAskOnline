#!/usr/bin/env python3
""" Vote model definition """
from models.base import Base, db


class Vote(Base):
    """ Vode model """
    __tablename__ = 'votes'

    is_upvote = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.String(256), nullable=False)
    parent_type = db.Column(db.String(256), nullable=False)

    user = db.relationship('User',
                           backref=db.backref('votes', lazy=True))

    def __init__(self, is_upvote):
        """ Vote Initializer """
        self.is_upvote = is_upvote
