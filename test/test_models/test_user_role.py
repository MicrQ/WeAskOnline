#!/usr/bin/env python3
""" test for UserRole model """
from models.base import db
from models.role import Role
from models.user import User
from models.user_role import UserRole
from models.country import Country
from flask import Flask
import unittest
from sqlalchemy import text
from datetime import datetime, timezone


class testQuestionTagModel(unittest.TestCase):
    """ test class for UserRole model """

    def setUp(self):
        """ setup the in memory db and create the table """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.app_context().push()

        db.init_app(self.app)
        with self.app.app_context():
            db.session.execute(text('PRAGMA foreign_keys = ON'))
            db.create_all()

    def tearDown(self):
        """ teardown the db and drop the table """
        db.session.remove()
        db.drop_all()

    def test_create_user_role(self):
        """ test creating new user role model """
        new_country = Country(name='France')
        db.session.add(new_country)
        db.session.commit()

        country = db.session.query(Country).filter_by(name='France').first()
        self.assertIsNotNone(country)

        now = datetime.now(timezone.utc)
        new_User = User(
            firstname="John",
            lastname="Doe",
            bio="Software Engineer",
            username="johndoe",
            email="john@example.com",
            password="hashed_password",
            created_at=now,
            updated_at=now,
            country_id=country.id
        )

        db.session.add(new_User)
        db.session.commit()

        user = db.session.query(User).filter_by(username='johndoe').first()
        self.assertIsNotNone(user)

        new_role = Role(
            name="admin"
        )
        db.session.add(new_role)
        db.session.commit()

        role = db.session.query(Role).filter_by(name="admin").first()
        self.assertIsNotNone(role)

        new_user_role = UserRole(
            user_id=user.id,
            role_id=role.id
        )
        db.session.add(new_user_role)
        db.session.commit()

        user_role = db.session.query(
            UserRole).filter_by(user_id=user.id).first()
        self.assertIsNotNone(user_role)

        # test with invalid user_id
        with self.assertRaises(Exception):
            new_user_role = UserRole(
                user_id=-1,
                role_id=role.id
            )
            db.session.add(new_user_role)
            db.session.commit()
        db.session.rollback()

        # test with invalid role_id
        with self.assertRaises(Exception):
            new_user_role = UserRole(
                user_id=user.id,
                role_id=-1
            )
            db.session.add(new_user_role)
            db.session.commit()
        db.session.rollback()


if __name__ == '__main__':
    unittest.main()
