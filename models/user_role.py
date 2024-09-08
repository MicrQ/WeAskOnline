#!/usr/bin/env python3
""" UserRoles model definition """
from models.base import Base, db
from models.user import User
from models.role import Role


class UserRole(Base):
    """ UserRole model """
    __tablename__ = 'user_roles'

    user_id = db.Column(db.String(256),
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    role_id = db.Column(db.String(256),
                        db.ForeignKey('roles.id', ondelete='CASCADE'),
                        nullable=False)
    user = db.relationship('User',
                           backref=db.backref('user_roles', lazy=True))
    role = db.relationship('Role',
                           backref=db.backref('user_roles', lazy=True))

    def __init__(self, user_id, role_id):
        """ UserRole Initializer """
        self.user_id = user_id
        self.role_id = role_id