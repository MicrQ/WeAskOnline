#!/usr/bin/env python3
""" Replay model definition """
from models.base import Base, db
from models.comment import Comment
from models.user import User


class Reply(Base):
    """ Base Model """
    __tablename__ = 'replies'
    body = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    isEdited = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    comment_id = db.Column(db.String(256), db.ForeignKey(
        'comments.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('replies', lazy=True))
    comment = db.relationship('Comment',
                              backref=db.backref('replies', lazy=True))

    def __init__(self, body, created_at,
                 isEdited, user_id, comment_id):
        """ Reply model initializer """
        self.body = body
        self.created_at = created_at
        self.user_id = user_id
        self.comment_id = comment_id
        self.isEdited = isEdited