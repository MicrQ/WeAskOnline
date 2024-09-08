#!/usr/bin/env python3
""" QuestionTag model implementation """
from models.base import Base, db
from models.question import Question
from models.tag import Tag


class QuestionTag(Base):
    """ QuestionTag Model """
    __tablename__ = 'question_tags'

    question_id = db.Column(db.String(256),
                            db.ForeignKey('questions.id'), primary_key=True)
    tag_id = db.Column(db.String(256),
                       db.ForeignKey('tags.id'), primary_key=True)

    question = db.relationship('Question',
                               backref=db.backref(
                                   'question_tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref(
        'question_tags', lazy=True))

    def __init__(self, question_id, tag_id):
        """ QuestionTag Initializer """
        self.question_id = question_id
        self.tag_id = tag_id
