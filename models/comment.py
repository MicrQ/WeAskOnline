#!/usr/bin/env python3
""" Question model definition """
from models.base import db
from models.user import User
from models.question import Question


class Comment(db.Model):
    """ Comment model """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    body = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    isEdited = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    question_id = db.Column(db.String(256), db.ForeignKey(
        'questions.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User',
                           backref=db.backref('comments', lazy=True))
    question = db.relationship('Question',
                               backref=db.backref('comments', lazy=True))

    def __init__(self, body, created_at,
                 user_id, question_id):
        """ Comment model initializer """
        self.body = body
        self.created_at = created_at
        self.user_id = user_id
        self.question_id = question_id
