#!/usr/bin/env python3
""" test for User model """
from models.base import db
from models.user import User
from models.country import Country
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import unittest
from datetime import datetime, timezone
from sqlalchemy import text


class testUserModel(unittest.TestCase):
    """ test class for User model """

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

    def test_User_creation(self):
        """ test creating new User """
        new_country = Country(name="France")
        db.session.add(new_country)
        db.session.commit()

        country = db.session.query(Country).filter_by(name="France").first()
        self.assertIsNotNone(country)

        new_User = User(
            firstname="John",
            lastname="Doe",
            bio="Software Engineer",
            username="johndoe",
            email="john@example.com",
            password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            country_id=country.id
        )
        db.session.add(new_User)
        db.session.commit()

    def test_Invalid_country_id(self):
        """ test creating new User with invalid country id """
        new_User = User(
            firstname="John",
            lastname="Doe",
            bio="Software Engineer",
            username="johndoe",
            email="john@example.com",
            password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            country_id=56  # random country id
        )
        db.session.add(new_User)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_Existing_Email(self):
        """ test creating new User with existing email """
        new_country = Country(name="France")
        db.session.add(new_country)
        db.session.commit()

        country = db.session.query(Country).filter_by(name="France").first()
        self.assertIsNotNone(country)

        new_User = User(
            firstname="John",
            lastname="Doe",
            bio="Software Engineer",
            username="johndoe",
            email="john@example.com",
            password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            country_id=country.id
        )
        db.session.add(new_User)
        db.session.commit()

        duplicate_User = User(
            firstname="Mike",
            lastname="Tyson",
            bio="Machine Engineer",
            username="miketyson",
            # trying to register user with existing email
            email="john@example.com",
            password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            country_id=country.id
        )
        db.session.add(duplicate_User)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_Existing_Username(self):
        """ test creating new User with existing username """
        new_country = Country(name="France")
        db.session.add(new_country)
        db.session.commit()

        country = db.session.query(Country).filter_by(name="France").first()
        self.assertIsNotNone(country)

        new_User = User(
            firstname="John",
            lastname="Doe",
            bio="Software Engineer",
            username="johndoe",
            email="john@example.com",
            password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            country_id=country.id
        )
        db.session.add(new_User)
        db.session.commit()

        duplicate_User = User(
            firstname="Mike",
            lastname="Tyson",
            bio="Machine Engineer",
            # trying to register user with existing email
            username="johndoe",
            email="mike@example.com",
            password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            country_id=country.id
        )
        db.session.add(duplicate_User)
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
