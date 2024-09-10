#!/usr/bin/env python3
""" test for Question model """
from models.base import db
from models.user import User
from models.question import Question
from models.country import Country
from flask import Flask
import unittest
from datetime import datetime, timezone
from sqlalchemy import text


class testQuestionModel(unittest.TestCase):
    """ test class for Question model """

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

    def test_create_question(self):
        """ test create question """
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

        new_question = Question(
            title="What is python",
            body="I want someone to tell me what python is.",
            user_id=user.id,
            created_at=now,
            updated_at=now,
        )

        db.session.add(new_question)
        db.session.commit()

        question = db.session.query(Question).filter_by(created_at=now).first
        self.assertIsNotNone(question)

    def test_invalid_user_id(self):
        """ test invalid user id """
        now = datetime.now(timezone.utc)
        new_question = Question(
            title="What is python",
            body="I want someone to tell me what python is.",
            user_id=-1,
            created_at=now,
            updated_at=now,
        )

        db.session.add(new_question)
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
