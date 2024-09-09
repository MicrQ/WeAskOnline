#!/usr/bin/env python3
""" QuestionTag model implementation """
from models.base import db
from models.question import Question
from models.tag import Tag


class QuestionTag(db.Model):
    """ QuestionTag Model """
    __tablename__ = 'question_tags'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    question_id = db.Column(db.String(256),
                            db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.String(256),
                       db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

    question = db.relationship('Question',
                               backref=db.backref(
                                   'question_tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref(
        'question_tags', lazy=True))

    def __init__(self, question_id, tag_id):
        """ QuestionTag Initializer """
        self.question_id = question_id
        self.tag_id = tag_id
