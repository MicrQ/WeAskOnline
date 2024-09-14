#!/usr/bin/env python3
""" Initialization for models """

from api.v1 import db, User, Country
from .base import db
from .user import User
from .country import Country
from .question import Question
from .question_tag import QuestionTag
from .role import Role
from .tag import Tag
from .user_role import UserRole
from .vote import Vote
from .reply import Reply
from .comment import Comment
from .report import Report

# Export db and models to be used elsewhere
__all__ = ['db', 'User', 'Country', 'Question', 'QuestionTag', 'Role', 'Tag', 'UserRole', 'Vote', 'Reply', 'Comment', 'Report']
