#!/usr/bin/env python3
""" Replay model definition """
from models.base import db
from models.comment import Comment
from models.user import User
from datetime import datetime, timezone


class Reply(db.Model):
    """ Base Model """
    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    body = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now(timezone.utc))
    isEdited = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey(
        'comments.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('replies', lazy=True))
    comment = db.relationship('Comment',
                              backref=db.backref('replies', lazy=True))

    def __init__(self, body, user_id,
                 comment_id):
        """ Reply model initializer """
        self.body = body
        self.user_id = user_id
        self.comment_id = comment_id

    def to_dict(self):
        """ returns the dictionary version of the model """
        return {
            'id': self.id,
            'body': self.body,
            'created_at': self.created_at,
            'isEdited': self.isEdited,
            'user_id': self.user_id,
            'comment_id': self.comment_id
        }
