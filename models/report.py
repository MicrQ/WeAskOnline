#!/usr/bin/python3
""" Report model definition """
from models.base import db


class Report(db.Model):
    """ Report model """
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    reason = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    isResolved = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    parent_id = db.Column(db.String(256), nullable=False)
    parent_type = db.Column(db.String(256), nullable=False)

    user = db.relationship('User',
                           backref=db.backref('reports', lazy=True))

    def __init__(self, reason, created_at,
                 parent_id, parent_type,
                 user_id):
        """ Report Initializer """
        self.reason = reason
        self.created_at = created_at
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.user_id = user_id
