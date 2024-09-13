#!/usr/bin/env python3
""" Initialization for models """

from .base import db  # Import db from base
from .user import User  # Import your User model (and any other models)

# Export db and models to be used elsewhere
__all__ = ['db', 'User']
